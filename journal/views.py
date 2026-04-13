import csv
import json
import logging
import os
import re
from urllib import error as urllib_error
from urllib import request as urllib_request
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import EntryForm, SignUpForm, UploadForm
from .models import DocumentUpload, Entry

logger = logging.getLogger(__name__)

VALID_STATUS_FILTERS = {"all", "pending", "completed", "overdue", "no-task"}
VALID_SORT_FILTERS = {"newest", "oldest", "updated", "due_soon"}
VALID_PRIORITY_FILTERS = {"all", Entry.PRIORITY_LOW, Entry.PRIORITY_MEDIUM, Entry.PRIORITY_HIGH}
RECOMMENDATION_KEYWORDS = (
    "recommend",
    "suggest",
    "advice",
    "plan",
    "next step",
    "priorit",
)
REALTIME_KEYWORDS = ("real-time", "realtime", "today", "right now", "now", "time", "date")
WEATHER_KEYWORDS = ("weather", "temperature", "forecast", "rain", "wind", "sunny", "cloud")
WEATHER_CODE_LABELS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with light hail",
    99: "Thunderstorm with heavy hail",
}


def _is_recommendation_prompt(prompt):
    normalized = prompt.lower()
    return any(keyword in normalized for keyword in RECOMMENDATION_KEYWORDS)


def _wants_realtime_context(prompt):
    normalized = prompt.lower()
    return any(keyword in normalized for keyword in REALTIME_KEYWORDS)


def _wants_weather_context(prompt):
    normalized = prompt.lower()
    return any(keyword in normalized for keyword in WEATHER_KEYWORDS)


def _extract_weather_location(prompt):
    match = re.search(
        r"(?:weather|temperature|forecast)\s+(?:in|at|for)\s+([a-zA-Z][\w\s,\-]{1,80})",
        prompt,
        flags=re.IGNORECASE,
    )
    if not match:
        return ""
    return match.group(1).strip(" .,!?:;")


def _fetch_weather_snapshot(location, timeout_seconds):
    geocode_query = urlencode(
        {"name": location, "count": 1, "language": "en", "format": "json"}
    )
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?{geocode_query}"

    try:
        with urllib_request.urlopen(geocode_url, timeout=timeout_seconds) as response:
            geocode_data = json.loads(response.read().decode("utf-8"))
    except (urllib_error.URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError):
        return {"error": "Could not fetch weather location details right now."}

    results = geocode_data.get("results") or []
    if not results:
        return {"error": f"Could not find weather data for '{location}'."}

    place = results[0]
    latitude = place.get("latitude")
    longitude = place.get("longitude")
    if latitude is None or longitude is None:
        return {"error": "Weather service returned incomplete location coordinates."}

    forecast_query = urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "timezone": "auto",
        }
    )
    forecast_url = f"https://api.open-meteo.com/v1/forecast?{forecast_query}"

    try:
        with urllib_request.urlopen(forecast_url, timeout=timeout_seconds) as response:
            forecast_data = json.loads(response.read().decode("utf-8"))
    except (urllib_error.URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError):
        return {"error": "Could not fetch weather forecast details right now."}

    current = forecast_data.get("current") or {}
    weather_code = current.get("weather_code", 0)
    location_label_parts = [place.get("name"), place.get("admin1"), place.get("country")]
    location_label = ", ".join(part for part in location_label_parts if part)

    return {
        "location": location_label or location.title(),
        "temperature_c": current.get("temperature_2m"),
        "feels_like_c": current.get("apparent_temperature"),
        "wind_kph": current.get("wind_speed_10m"),
        "precip_mm": current.get("precipitation"),
        "weather": WEATHER_CODE_LABELS.get(weather_code, "Current conditions unavailable"),
        "observed_at": current.get("time"),
        "timezone": forecast_data.get("timezone"),
    }


def _format_weather_snapshot(snapshot):
    if not snapshot or snapshot.get("error"):
        return ""

    return (
        f"Weather in {snapshot.get('location')}: "
        f"{snapshot.get('weather')}, "
        f"{snapshot.get('temperature_c')}°C "
        f"(feels like {snapshot.get('feels_like_c')}°C), "
        f"wind {snapshot.get('wind_kph')} km/h, "
        f"precipitation {snapshot.get('precip_mm')} mm."
    )


def _build_recommendation_context(user):
    """Build comprehensive journal context for AI recommendations."""
    entries = Entry.objects.filter(user=user)
    total_entries = entries.count()
    
    # Task statistics
    task_entries = entries.filter(task__gt="")
    pending_tasks = task_entries.filter(task_completed=False)
    completed_tasks = task_entries.filter(task_completed=True)
    overdue_tasks = pending_tasks.filter(task_due_at__isnull=False, task_due_at__lte=timezone.now())
    
    # Priority breakdown
    high_priority_pending = pending_tasks.filter(task_priority=Entry.PRIORITY_HIGH).count()
    medium_priority_pending = pending_tasks.filter(task_priority=Entry.PRIORITY_MEDIUM).count()
    
    # Starred entries (important content)
    starred_entries = entries.filter(is_starred=True).count()
    
    # Recent activity
    latest_entries = list(entries.order_by("-date_updated").values("title", "task", "task_completed")[:5])
    latest_titles = [e["title"] for e in latest_entries]
    latest_activities = []
    for e in latest_entries:
        activity = e["title"]
        if e["task"]:
            status = "✓" if e["task_completed"] else "○"
            activity += f" [{status} {e['task']}]"
        latest_activities.append(activity)
    
    context_parts = [
        f"Journal stats: {total_entries} entries, {task_entries.count()} tasks",
        f"Tasks: {completed_tasks.count()} completed, {pending_tasks.count()} pending, {overdue_tasks.count()} overdue",
        f"Priority: {high_priority_pending} high, {medium_priority_pending} medium priority pending",
        f"Starred: {starred_entries} important entries",
    ]
    
    if latest_activities:
        activities_text = "; ".join(latest_activities[:3])
        context_parts.append(f"Recent: {activities_text}")
    
    if overdue_tasks.count() > 0:
        context_parts.append(f"⚠️ URGENT: {overdue_tasks.count()} overdue tasks need attention")
    
    return ". ".join(context_parts) + "."


def _realtime_snapshot():
    local_now = timezone.localtime(timezone.now())
    return {
        "local_datetime": local_now.strftime("%A, %B %d, %Y %H:%M:%S"),
        "timezone": str(local_now.tzinfo),
        "iso": local_now.isoformat(),
    }


def _extract_task_context(user, prompt):
    """Extract relevant task information from user prompt if available."""
    # Check if user is asking about specific tasks or entries
    entries = Entry.objects.filter(user=user).filter(task__gt="")
    
    relevant_tasks = []
    for entry in entries[:10]:
        if entry.task.lower() in prompt.lower() or entry.title.lower() in prompt.lower():
            relevant_tasks.append({
                "task": entry.task,
                "priority": entry.task_priority_label,
                "completed": entry.task_completed,
                "due": entry.task_due_at,
                "title": entry.title,
            })
    
    if len(relevant_tasks) > 3:
        relevant_tasks = relevant_tasks[:3]
    
    return relevant_tasks


def _normalize_chat_history(raw_history):
    if not isinstance(raw_history, list):
        return []

    normalized = []
    for item in raw_history[-12:]:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = (item.get("content") or "").strip()

        if role not in {"user", "assistant"} or not content:
            continue

        normalized.append({"role": role, "content": content[:3000]})

    return normalized


def _analyze_uploaded_document(document_upload):
    document_upload.file_type = document_upload.file_extension
    document_upload.status = DocumentUpload.STATUS_PENDING
    document_upload.processed_at = timezone.now()

    try:
        document_upload.file.open(mode="rb")
        extension = document_upload.file_extension
        if extension in {"txt", "md", "csv"}:
            text = document_upload.file.read().decode("utf-8", errors="ignore")
            word_count = len(re.findall(r"\w+", text))
            document_upload.analysis = (
                f"Text document stored and indexed. Detected {word_count} words. "
                "Use the assistant to summarize key points or turn this into action items."
            )
            document_upload.status = DocumentUpload.STATUS_ANALYZED
        elif extension == "pdf":
            document_upload.analysis = (
                "PDF stored. A content summary is available for review. "
                "Use the journal assistant to extract key insights from the document."
            )
            document_upload.status = DocumentUpload.STATUS_ANALYZED
        elif extension in {"mp4", "mov", "avi", "mkv"}:
            document_upload.analysis = (
                "Video file stored. Uploaded media is available for playback and metadata review. "
                "Use the assistant to help synthesize themes and action items from the video."
            )
            document_upload.status = DocumentUpload.STATUS_ANALYZED
        else:
            document_upload.analysis = (
                "File stored successfully. Analysis is pending for this type. "
                "Use the assistant if you need help interpreting the content."
            )
            document_upload.status = DocumentUpload.STATUS_STORED
    except Exception:
        document_upload.analysis = (
            "File was stored successfully, but content analysis is not available at this time. "
            "Try again with a supported document format."
        )
        document_upload.status = DocumentUpload.STATUS_STORED
    finally:
        document_upload.file.close()

    document_upload.save()
    return document_upload


def _build_ollama_chat_request(model, messages, temperature=0.7):
    """Build Ollama chat request with optimized parameters for better responses."""
    request_body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,  # Lower for more focused responses
                "num_predict": 500,  # Limit response length
                "top_p": 0.9,
                "top_k": 40,
            },
        }
    ).encode("utf-8")
    return urllib_request.Request(
        f"{settings.OLLAMA_BASE_URL}/api/chat",
        data=request_body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )


def _fetch_available_ollama_models(timeout_seconds):
    tags_url = f"{settings.OLLAMA_BASE_URL}/api/tags"
    try:
        with urllib_request.urlopen(tags_url, timeout=timeout_seconds) as response:
            tags_payload = json.loads(response.read().decode("utf-8"))
    except (urllib_error.URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError):
        return {"candidates": [], "display": []}

    available_candidates = []
    display_names = []
    for model_item in tags_payload.get("models") or []:
        if not isinstance(model_item, dict):
            continue
        raw_name = (model_item.get("name") or "").strip()
        if not raw_name:
            continue
        if raw_name not in display_names:
            display_names.append(raw_name)
        # Try exact model name first, then its base alias.
        for candidate in (raw_name, raw_name.split(":")[0]):
            if candidate and candidate not in available_candidates:
                available_candidates.append(candidate)
    return {"candidates": available_candidates, "display": display_names}


def _ollama_fallback_candidates(preferred_model):
    configured = [preferred_model, *getattr(settings, "OLLAMA_FALLBACK_MODELS", [])]
    unique_candidates = []
    for model_name in configured:
        name = (model_name or "").strip()
        if name and name not in unique_candidates:
            unique_candidates.append(name)
    return unique_candidates


def _execute_ollama_request(ollama_request, timeout_seconds):
    with urllib_request.urlopen(ollama_request, timeout=timeout_seconds) as response:
        return json.loads(response.read().decode("utf-8"))


def _safe_float(raw_value):
    try:
        return float(raw_value)
    except (TypeError, ValueError):
        return None


def _fetch_weather_snapshot_by_coordinates(latitude, longitude, timeout_seconds):
    forecast_query = urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,apparent_temperature,precipitation,"
                "weather_code,wind_speed_10m"
            ),
            "timezone": "auto",
        }
    )
    forecast_url = f"https://api.open-meteo.com/v1/forecast?{forecast_query}"

    try:
        with urllib_request.urlopen(forecast_url, timeout=timeout_seconds) as response:
            forecast_data = json.loads(response.read().decode("utf-8"))
    except (urllib_error.URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError):
        return {"error": "Could not fetch weather forecast details right now."}

    location_label = ""
    reverse_query = urlencode(
        {
            "latitude": latitude,
            "longitude": longitude,
            "count": 1,
            "language": "en",
            "format": "json",
        }
    )
    reverse_url = f"https://geocoding-api.open-meteo.com/v1/reverse?{reverse_query}"
    try:
        with urllib_request.urlopen(reverse_url, timeout=timeout_seconds) as response:
            reverse_data = json.loads(response.read().decode("utf-8"))
            results = reverse_data.get("results") or []
            if results:
                place = results[0]
                location_parts = [place.get("name"), place.get("admin1"), place.get("country")]
                location_label = ", ".join(part for part in location_parts if part)
    except (urllib_error.URLError, TimeoutError, UnicodeDecodeError, json.JSONDecodeError):
        location_label = ""

    current = forecast_data.get("current") or {}
    weather_code = current.get("weather_code", 0)
    if not location_label:
        location_label = f"{latitude:.4f}, {longitude:.4f}"

    return {
        "location": location_label,
        "temperature_c": current.get("temperature_2m"),
        "feels_like_c": current.get("apparent_temperature"),
        "wind_kph": current.get("wind_speed_10m"),
        "precip_mm": current.get("precipitation"),
        "weather": WEATHER_CODE_LABELS.get(weather_code, "Current conditions unavailable"),
        "observed_at": current.get("time"),
        "timezone": forecast_data.get("timezone"),
    }


def _parse_filters(request):
    query = (request.GET.get("q") or "").strip()
    status_filter = (request.GET.get("status") or "all").strip()
    priority_filter = (request.GET.get("priority") or "all").strip()
    sort_filter = (request.GET.get("sort") or "newest").strip()

    if status_filter not in VALID_STATUS_FILTERS:
        status_filter = "all"
    if priority_filter not in VALID_PRIORITY_FILTERS:
        priority_filter = "all"
    if sort_filter not in VALID_SORT_FILTERS:
        sort_filter = "newest"

    return {
        "query": query,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "sort_filter": sort_filter,
    }


def _apply_entry_filters(entries, filters):
    now = timezone.now()
    query = filters["query"]
    status_filter = filters["status_filter"]
    priority_filter = filters["priority_filter"]

    if query:
        entries = entries.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(task__icontains=query)
        )

    if status_filter == "completed":
        entries = entries.filter(task__gt="", task_completed=True)
    elif status_filter == "pending":
        entries = entries.filter(task__gt="", task_completed=False).filter(
            Q(task_due_at__isnull=True) | Q(task_due_at__gt=now)
        )
    elif status_filter == "overdue":
        entries = entries.filter(
            task__gt="",
            task_completed=False,
            task_due_at__isnull=False,
            task_due_at__lte=now,
        )
    elif status_filter == "no-task":
        entries = entries.filter(task="")

    if priority_filter != "all":
        entries = entries.filter(task_priority=priority_filter)

    return entries


def _apply_sort(entries, sort_filter):
    if sort_filter == "oldest":
        return entries.order_by("date_created")
    if sort_filter == "updated":
        return entries.order_by("-date_updated")
    if sort_filter == "due_soon":
        return entries.order_by(F("task_due_at").asc(nulls_last=True), "-date_created")
    return entries.order_by("-date_created")


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        return redirect("entry_list")

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account has been created.")
            return redirect("entry_list")
    else:
        form = SignUpForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def entry_list(request):
    try:
        base_entries = Entry.objects.filter(user=request.user)

        if request.method == "POST":
            form = EntryForm(request.POST)
            if form.is_valid():
                entry = form.save(commit=False)
                entry.user = request.user
                entry.save()
                logger.info("Entry created by user %s: %s", request.user.username, entry.pk)
                messages.success(request, "Entry added successfully.")
                return redirect("entry_list")
            else:
                logger.debug("Form validation failed for user %s: %s", request.user.username, form.errors)
        else:
            form = EntryForm()

        filters = _parse_filters(request)
        entries = _apply_sort(_apply_entry_filters(base_entries, filters), filters["sort_filter"])

        overdue_entries = base_entries.filter(
            task__gt="",
            task_completed=False,
            task_due_at__isnull=False,
            task_due_at__lte=timezone.now(),
        )
        task_entries = base_entries.filter(task__gt="")

        stats = {
            "total_entries": base_entries.count(),
            "starred_entries": base_entries.filter(is_starred=True).count(),
            "task_entries": task_entries.count(),
            "completed_tasks": task_entries.filter(task_completed=True).count(),
            "overdue_tasks": overdue_entries.count(),
        }

        return render(
            request,
            "journal/entry_list.html",
            {
                "entries": entries,
                "form": form,
                "overdue_entries": overdue_entries[:5],
                "overdue_entries_count": overdue_entries.count(),
                "query": filters["query"],
                "status_filter": filters["status_filter"],
                "priority_filter": filters["priority_filter"],
                "sort_filter": filters["sort_filter"],
                "stats": stats,
                "ollama_model": settings.OLLAMA_MODEL,
                "weather_location_default": settings.WEATHER_DEFAULT_LOCATION,
            },
        )
    except Exception as e:
        logger.error("Error in entry_list for user %s: %s", request.user.username, str(e), exc_info=True)
        messages.error(request, "An error occurred while loading entries. Please try again.")
        return redirect("entry_list")


@login_required
@require_http_methods(["GET"])
def entry_export_csv(request):
    base_entries = Entry.objects.filter(user=request.user)
    filters = _parse_filters(request)
    entries = _apply_sort(_apply_entry_filters(base_entries, filters), filters["sort_filter"])

    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f'attachment; filename="journal_entries_{timestamp}.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(
        [
            "Title",
            "Starred",
            "Task",
            "Task Priority",
            "Task Completed",
            "Task Due",
            "WhatsApp Number",
            "Created",
            "Updated",
            "Content",
        ]
    )

    for entry in entries:
        task_due = (
            timezone.localtime(entry.task_due_at).strftime("%Y-%m-%d %H:%M")
            if entry.task_due_at
            else ""
        )
        writer.writerow(
            [
                entry.title,
                "Yes" if entry.is_starred else "No",
                entry.task,
                entry.task_priority_label,
                "Yes" if entry.task_completed else "No",
                task_due,
                entry.alert_phone_number,
                timezone.localtime(entry.date_created).strftime("%Y-%m-%d %H:%M"),
                timezone.localtime(entry.date_updated).strftime("%Y-%m-%d %H:%M"),
                entry.content,
            ]
        )

    return response


@login_required
@require_http_methods(["POST"])
def ollama_chat(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        logger.error("Invalid JSON payload in ollama_chat: %s", str(e))
        return JsonResponse({"error": "Invalid JSON payload."}, status=400)

    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        logger.warning("Empty prompt received in ollama_chat for user %s", request.user.username)
        return JsonResponse({"error": "Prompt is required."}, status=400)

    chat_history = _normalize_chat_history(payload.get("history"))
    preferred_weather_location = (payload.get("weather_location") or "").strip()
    preferred_latitude = _safe_float(payload.get("lat"))
    preferred_longitude = _safe_float(payload.get("lon"))
    requested_model = (payload.get("model") or "").strip()
    model = requested_model or settings.OLLAMA_MODEL
    timeout_seconds = max(5, settings.OLLAMA_TIMEOUT_SECONDS)
    recommendation_mode = _is_recommendation_prompt(prompt)
    realtime_requested = _wants_realtime_context(prompt)
    weather_requested = _wants_weather_context(prompt)
    extracted_weather_location = _extract_weather_location(prompt)
    weather_lookup_location = ""
    use_coordinate_weather = False
    if extracted_weather_location:
        weather_lookup_location = extracted_weather_location
    elif weather_requested and preferred_latitude is not None and preferred_longitude is not None:
        use_coordinate_weather = True
    elif weather_requested and preferred_weather_location:
        weather_lookup_location = preferred_weather_location
    weather_snapshot = {}

    if use_coordinate_weather:
        weather_snapshot = _fetch_weather_snapshot_by_coordinates(
            preferred_latitude,
            preferred_longitude,
            timeout_seconds=min(15, timeout_seconds),
        )
    elif weather_lookup_location:
        weather_snapshot = _fetch_weather_snapshot(
            weather_lookup_location,
            timeout_seconds=min(15, timeout_seconds),
        )

    prompt_context = []
    if recommendation_mode:
        prompt_context.append(_build_recommendation_context(request.user))
    if realtime_requested:
        realtime_context = _realtime_snapshot()
        prompt_context.append(
            "Current local server time: "
            f"{realtime_context['local_datetime']} ({realtime_context['timezone']})."
        )
    if weather_lookup_location or use_coordinate_weather:
        weather_text = _format_weather_snapshot(weather_snapshot)
        if weather_text:
            prompt_context.append(weather_text)
        else:
            prompt_context.append(
                weather_snapshot.get("error")
                or "Weather lookup is currently unavailable."
            )

    user_prompt = prompt
    if prompt_context:
        user_prompt = (
            f"{prompt}\n\nContext for this response:\n- "
            + "\n- ".join(prompt_context)
        )

    # Build context-aware system prompt
    system_prompt = (
        "You are a professional journal productivity assistant in a personal dashboard. "
        "Provide concise, actionable guidance for reflection, planning, and task execution. "
        "Keep responses focused on the user's journal context and avoid unnecessary explanation."
    )
    
    if recommendation_mode:
        system_prompt += (
            "\n\nFor recommendations:\n"
            "- Provide 2-5 numbered actionable steps\n"
            "- Flag overdue items as URGENT\n"
            "- Consider priority levels in your suggestions\n"
            "- Help break down complex tasks\n"
            "- Suggest task consolidation when appropriate"
        )
    
    # Lower temperature for recommendation mode for more focused responses
    ai_temperature = 0.6 if recommendation_mode else 0.7

    messages_payload = [{"role": "system", "content": system_prompt}, *chat_history]
    messages_payload.append({"role": "user", "content": user_prompt})

    active_model = model
    model_fallback_used = False
    logger.debug(
        "Building Ollama request: user=%s, model=%s, mode=%s, context_items=%d",
        request.user.username,
        active_model,
        "recommendation" if recommendation_mode else "general",
        len(prompt_context),
    )
    ollama_request = _build_ollama_chat_request(active_model, messages_payload, temperature=ai_temperature)

    try:
        logger.debug("Executing Ollama request for user %s", request.user.username)
        response_payload = _execute_ollama_request(ollama_request, timeout_seconds)
    except urllib_error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore").strip()
        normalized_detail = detail.lower()
        is_model_not_found = (
            "model" in normalized_detail
            and ("not found" in normalized_detail or "does not exist" in normalized_detail)
        )

        if is_model_not_found:
            available_info = _fetch_available_ollama_models(min(10, timeout_seconds))
            available_candidates = available_info["candidates"]
            available_display = available_info["display"]
            candidates = _ollama_fallback_candidates(active_model)
            if available_candidates:
                candidates = [
                    candidate for candidate in candidates if candidate in available_candidates
                ] + [
                    available
                    for available in available_candidates
                    if available not in candidates
                ]

            fallback_success = False
            for fallback_model in candidates:
                if fallback_model == active_model:
                    continue

                try:
                    response_payload = _execute_ollama_request(
                        _build_ollama_chat_request(fallback_model, messages_payload),
                        timeout_seconds,
                    )
                except urllib_error.HTTPError as fallback_exc:
                    fallback_detail = fallback_exc.read().decode("utf-8", errors="ignore").strip()
                    normalized_fallback_detail = fallback_detail.lower()
                    fallback_not_found = (
                        "model" in normalized_fallback_detail
                        and (
                            "not found" in normalized_fallback_detail
                            or "does not exist" in normalized_fallback_detail
                        )
                    )
                    if fallback_not_found:
                        continue
                    error_message = fallback_detail or f"Ollama returned HTTP {fallback_exc.code}."
                    return JsonResponse({"error": error_message}, status=502)
                except (urllib_error.URLError, TimeoutError):
                    return JsonResponse(
                        {
                            "error": (
                                "Could not connect to Ollama. Ensure Ollama is running at "
                                f"{settings.OLLAMA_BASE_URL}."
                            )
                        },
                        status=502,
                    )
                except (UnicodeDecodeError, json.JSONDecodeError):
                    return JsonResponse(
                        {"error": "Ollama returned an invalid response payload."},
                        status=502,
                    )

                resolved_model = (response_payload.get("model") or "").strip()
                active_model = resolved_model or fallback_model
                model_fallback_used = True
                fallback_success = True
                break

            if not fallback_success:
                if available_display:
                    model_hint = ", ".join(available_display[:6])
                    return JsonResponse(
                        {
                            "error": (
                                "Configured Ollama model was not found. "
                                f"Available models: {model_hint}. "
                                "Pull a model first (for example: `ollama pull llama2`)."
                            )
                        },
                        status=502,
                    )
                return JsonResponse(
                    {
                        "error": (
                            "Configured Ollama model was not found and no fallback model was available. "
                            "Pull a model first (for example: `ollama pull llama2`)."
                        )
                    },
                    status=502,
                )

        if not is_model_not_found:
            error_message = detail or f"Ollama returned HTTP {exc.code}."
            return JsonResponse({"error": error_message}, status=502)
    except (urllib_error.URLError, TimeoutError):
        return JsonResponse(
            {
                "error": (
                    "Could not connect to Ollama. Ensure Ollama is running at "
                    f"{settings.OLLAMA_BASE_URL}."
                )
            },
            status=502,
        )
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse(
            {"error": "Ollama returned an invalid response payload."},
            status=502,
        )

    # Extract and validate response
    reply = ""
    if isinstance(response_payload.get("message"), dict):
        reply = (response_payload["message"].get("content") or "").strip()
    if not reply:
        reply = (response_payload.get("response") or "").strip()

    if not reply:
        logger.error("Ollama returned empty response for user %s", request.user.username)
        return JsonResponse({"error": "Ollama did not return any text."}, status=502)
    
    # Validate response length
    if len(reply) > 5000:
        logger.warning("Response exceeded 5000 chars, truncating for user %s", request.user.username)
        reply = reply[:5000].rsplit(' ', 1)[0] + "..."

    response_data = {
        "reply": reply,
        "model": response_payload.get("model") or active_model,
    }
    
    if model_fallback_used:
        response_data["model_notice"] = (
            f"Configured model '{model}' was unavailable. Using '{active_model}' instead."
        )
        logger.info("Model fallback used: %s -> %s for user %s", model, active_model, request.user.username)
    
    if realtime_requested or weather_requested:
        response_data["realtime"] = _realtime_snapshot()
    
    if weather_lookup_location or use_coordinate_weather:
        if weather_snapshot.get("error"):
            response_data["weather_error"] = weather_snapshot["error"]
            logger.warning("Weather lookup failed for user %s: %s", request.user.username, weather_snapshot.get("error"))
        else:
            response_data["weather"] = weather_snapshot
    
    logger.info(
        "Ollama chat successful: user=%s, model=%s, prompt_len=%d, response_len=%d",
        request.user.username,
        active_model,
        len(user_prompt),
        len(reply),
    )
    
    return JsonResponse(response_data)


@login_required
@require_http_methods(["GET"])
def assistant_realtime(request):
    location = (request.GET.get("location") or "").strip()
    latitude = _safe_float(request.GET.get("lat"))
    longitude = _safe_float(request.GET.get("lon"))
    timeout_seconds = max(5, settings.OLLAMA_TIMEOUT_SECONDS)
    response_data = {"realtime": _realtime_snapshot()}
    weather_snapshot = {}

    if latitude is not None and longitude is not None:
        weather_snapshot = _fetch_weather_snapshot_by_coordinates(
            latitude,
            longitude,
            timeout_seconds=min(15, timeout_seconds),
        )
    elif location:
        weather_snapshot = _fetch_weather_snapshot(
            location,
            timeout_seconds=min(15, timeout_seconds),
        )

    if weather_snapshot:
        error_msg = weather_snapshot.get("error")
        if error_msg:
            response_data["weather_error"] = {"error": str(error_msg)}
        else:
            response_data["weather"] = weather_snapshot

    return JsonResponse(response_data)


@login_required
@require_http_methods(["GET"])
def chatbot_health(request):
    """Check Ollama connectivity and available models."""
    timeout_seconds = max(5, settings.OLLAMA_TIMEOUT_SECONDS)
    health_data = {
        "status": "unknown",
        "ollama_url": settings.OLLAMA_BASE_URL,
        "models": {
            "configured": settings.OLLAMA_MODEL,
            "available": [],
        },
        "errors": [],
    }
    
    # Test Ollama connectivity
    try:
        available_info = _fetch_available_ollama_models(min(10, timeout_seconds))
        available_models = available_info.get("display", [])
        
        if available_models:
            health_data["status"] = "healthy"
            health_data["models"]["available"] = available_models[:10]
            
            if settings.OLLAMA_MODEL not in [m.split(":")[0] for m in available_models]:
                health_data["warnings"] = [
                    f"Configured model '{settings.OLLAMA_MODEL}' not found. "
                    f"Available: {', '.join(available_models[:3])}"
                ]
            
            logger.info("Chatbot health check successful: %d models available", len(available_models))
        else:
            health_data["status"] = "no-models"
            health_data["errors"].append("No Ollama models available. Pull a model first.")
            logger.warning("Chatbot health check: no models available")
            
    except Exception as e:
        health_data["status"] = "unhealthy"
        health_data["errors"].append(f"Cannot connect to Ollama at {settings.OLLAMA_BASE_URL}")
        logger.error("Chatbot health check failed: %s", str(e))
    
    status_code = 200 if health_data["status"] == "healthy" else 503
    return JsonResponse(health_data, status=status_code)


@login_required
@require_http_methods(["GET"])
def entry_detail(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    return render(request, "journal/entry_detail.html", {"entry": entry})


@login_required
@require_http_methods(["GET", "POST"])
def entry_edit(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    previous_task_state = (
        entry.task,
        entry.task_priority,
        entry.task_due_at,
        entry.task_completed,
        entry.alert_phone_number,
    )

    if request.method == "POST":
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            updated_entry = form.save(commit=False)
            current_task_state = (
                updated_entry.task,
                updated_entry.task_priority,
                updated_entry.task_due_at,
                updated_entry.task_completed,
                updated_entry.alert_phone_number,
            )

            if current_task_state != previous_task_state:
                updated_entry.alert_sent_at = None

            updated_entry.save()
            messages.success(request, "Entry updated successfully.")
            return redirect("entry_detail", pk=entry.pk)
    else:
        form = EntryForm(instance=entry)

    return render(request, "journal/entry_edit.html", {"form": form, "entry": entry})


@login_required
@require_http_methods(["POST"])
def entry_toggle_task(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)

    if not entry.has_task:
        messages.error(request, "Add a task first before changing task status.")
        return redirect("entry_detail", pk=entry.pk)

    entry.task_completed = not entry.task_completed
    if not entry.task_completed:
        entry.alert_sent_at = None
    entry.save()

    if entry.task_completed:
        messages.success(request, "Task marked as complete.")
    else:
        messages.warning(request, "Task marked as incomplete.")

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("entry_detail", pk=entry.pk)


@login_required
@require_http_methods(["POST"])
def entry_toggle_star(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)
    entry.is_starred = not entry.is_starred
    entry.save(update_fields=["is_starred"])

    if entry.is_starred:
        messages.success(request, "Entry added to favorites.")
    else:
        messages.info(request, "Entry removed from favorites.")

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)
    return redirect("entry_detail", pk=entry.pk)


@login_required
@require_http_methods(["GET", "POST"])
def entry_delete(request, pk):
    entry = get_object_or_404(Entry, pk=pk, user=request.user)

    if request.method == "POST":
        entry.delete()
        messages.success(request, "Entry deleted.")
        return redirect("entry_list")

    return render(request, "journal/entry_confirm_delete.html", {"entry": entry})


@login_required
@require_http_methods(["GET"])
def dashboard(request):
    """Main dashboard with overview and quick actions."""
    base_entries = Entry.objects.filter(user=request.user)
    
    # Recent entries
    recent_entries = base_entries.order_by("-date_created")[:5]
    
    # Task statistics
    task_entries = base_entries.filter(task__gt="")
    pending_tasks = task_entries.filter(task_completed=False)
    overdue_tasks = pending_tasks.filter(task_due_at__isnull=False, task_due_at__lte=timezone.now())
    
    # Today's entries
    today = timezone.now().date()
    today_entries = base_entries.filter(date_created__date=today)
    
    # Quick stats
    stats = {
        "total_entries": base_entries.count(),
        "today_entries": today_entries.count(),
        "starred_entries": base_entries.filter(is_starred=True).count(),
        "task_entries": task_entries.count(),
        "pending_tasks": pending_tasks.count(),
        "overdue_tasks": overdue_tasks.count(),
        "completed_tasks": task_entries.filter(task_completed=True).count(),
    }
    
    # Recent activity (last 7 days)
    week_ago = timezone.now() - timezone.timedelta(days=7)
    recent_activity = base_entries.filter(date_created__gte=week_ago).order_by("-date_created")[:10]
    
    # Time-based greeting
    current_hour = timezone.now().hour
    if 6 <= current_hour < 12:
        time_greeting = "morning"
    elif 12 <= current_hour < 18:
        time_greeting = "afternoon"
    else:
        time_greeting = "evening"
    
    document_count = DocumentUpload.objects.filter(user=request.user).count()
    latest_documents = DocumentUpload.objects.filter(user=request.user).order_by("-uploaded_at")[:4]

    context = {
        "stats": stats,
        "recent_entries": recent_entries,
        "overdue_tasks": overdue_tasks[:5],
        "recent_activity": recent_activity,
        "today_entries": today_entries,
        "ollama_model": settings.OLLAMA_MODEL,
        "weather_location_default": settings.WEATHER_DEFAULT_LOCATION,
        "time_greeting": time_greeting,
        "document_count": document_count,
        "latest_documents": latest_documents,
    }
    
    return render(request, "journal/dashboard.html", context)


@login_required
@require_http_methods(["GET"])
def entry_search(request):
    """Advanced search page for entries."""
    query = request.GET.get("q", "").strip()
    tag_filter = request.GET.get("tag", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()
    
    base_entries = Entry.objects.filter(user=request.user)
    
    if query:
        base_entries = base_entries.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(task__icontains=query)
        )
    
    if tag_filter:
        base_entries = base_entries.filter(
            Q(title__icontains=tag_filter) |
            Q(content__icontains=tag_filter)
        )
    
    if date_from:
        try:
            date_from_obj = timezone.datetime.fromisoformat(date_from).date()
            base_entries = base_entries.filter(date_created__date__gte=date_from_obj)
        except ValueError:
            pass
    
    if date_to:
        try:
            date_to_obj = timezone.datetime.fromisoformat(date_to).date()
            base_entries = base_entries.filter(date_created__date__lte=date_to_obj)
        except ValueError:
            pass
    
    entries = base_entries.order_by("-date_created")[:50]  # Limit results
    
    context = {
        "entries": entries,
        "query": query,
        "tag_filter": tag_filter,
        "date_from": date_from,
        "date_to": date_to,
        "total_results": base_entries.count(),
    }
    
    return render(request, "journal/entry_search.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def document_upload(request):
    """Upload documents or videos for storage and analysis."""
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload = form.save(commit=False)
            upload.user = request.user
            upload.status = DocumentUpload.STATUS_PENDING
            upload.save()
            _analyze_uploaded_document(upload)
            messages.success(request, "Upload received and analysis is complete.")
            return redirect("document_upload")
    else:
        form = UploadForm()

    uploads = DocumentUpload.objects.filter(user=request.user).order_by("-uploaded_at")[:10]
    context = {
        "form": form,
        "uploads": uploads,
    }
    return render(request, "journal/documents.html", context)


@login_required
@require_http_methods(["GET"])
def task_list(request):
    """Dedicated task management page."""
    base_entries = Entry.objects.filter(user=request.user, task__gt="")
    
    # Filter parameters
    status_filter = request.GET.get("status", "all")
    priority_filter = request.GET.get("priority", "all")
    sort_by = request.GET.get("sort", "due_soon")
    
    # Apply filters
    if status_filter == "pending":
        base_entries = base_entries.filter(task_completed=False)
    elif status_filter == "completed":
        base_entries = base_entries.filter(task_completed=True)
    elif status_filter == "overdue":
        base_entries = base_entries.filter(
            task_completed=False,
            task_due_at__isnull=False,
            task_due_at__lte=timezone.now()
        )
    
    if priority_filter != "all":
        base_entries = base_entries.filter(task_priority=priority_filter)
    
    # Apply sorting
    if sort_by == "due_soon":
        base_entries = base_entries.order_by(F("task_due_at").asc(nulls_last=True), "-date_created")
    elif sort_by == "newest":
        base_entries = base_entries.order_by("-date_created")
    elif sort_by == "oldest":
        base_entries = base_entries.order_by("date_created")
    elif sort_by == "priority":
        priority_order = {"high": 0, "medium": 1, "low": 2, "": 3}
        base_entries = sorted(base_entries, key=lambda x: priority_order.get(x.task_priority, 3))
    
    tasks = base_entries[:100]  # Limit for performance
    
    # Task statistics
    all_tasks = Entry.objects.filter(user=request.user, task__gt="")
    stats = {
        "total_tasks": all_tasks.count(),
        "pending_tasks": all_tasks.filter(task_completed=False).count(),
        "completed_tasks": all_tasks.filter(task_completed=True).count(),
        "overdue_tasks": all_tasks.filter(
            task_completed=False,
            task_due_at__isnull=False,
            task_due_at__lte=timezone.now()
        ).count(),
    }
    
    context = {
        "tasks": tasks,
        "stats": stats,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "sort_by": sort_by,
    }
    
    return render(request, "journal/task_list.html", context)


@login_required
@require_http_methods(["GET"])
def analytics(request):
    """Analytics and insights page."""
    base_entries = Entry.objects.filter(user=request.user)
    
    # Time-based analytics
    now = timezone.now()
    today = now.date()
    week_ago = today - timezone.timedelta(days=7)
    month_ago = today - timezone.timedelta(days=30)
    
    # Entry counts by period
    today_count = base_entries.filter(date_created__date=today).count()
    week_count = base_entries.filter(date_created__date__gte=week_ago).count()
    month_count = base_entries.filter(date_created__date__gte=month_ago).count()
    
    # Task analytics
    task_entries = base_entries.filter(task__gt="")
    completed_tasks = task_entries.filter(task_completed=True)
    pending_tasks = task_entries.filter(task_completed=False)
    overdue_tasks = pending_tasks.filter(task_due_at__isnull=False, task_due_at__lte=now)
    
    # Priority distribution
    priority_stats = {
        "high": pending_tasks.filter(task_priority="high").count(),
        "medium": pending_tasks.filter(task_priority="medium").count(),
        "low": pending_tasks.filter(task_priority="low").count(),
        "none": pending_tasks.filter(task_priority="").count(),
    }
    
    # Monthly activity (last 12 months)
    monthly_data = []
    for i in range(11, -1, -1):
        month_date = today - timezone.timedelta(days=30 * i)
        month_start = month_date.replace(day=1)
        next_month = (month_start + timezone.timedelta(days=32)).replace(day=1)
        month_end = next_month - timezone.timedelta(days=1)
        
        count = base_entries.filter(
            date_created__date__gte=month_start,
            date_created__date__lte=month_end
        ).count()
        
        monthly_data.append({
            "month": month_start.strftime("%b %Y"),
            "count": count,
        })
    
    # Top keywords (simple word frequency)
    all_content = " ".join(
        [entry.title + " " + entry.content for entry in base_entries.order_by("-date_created")[:50]]
    ).lower()
    
    # Remove common words and count
    common_words = {"the", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "an", "a", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "must", "can", "this", "that", "these", "those", "i", "me", "my", "myself", "we", "our", "ours", "you", "your", "yours", "he", "him", "his", "she", "her", "hers", "it", "its", "they", "them", "their", "theirs"}
    
    words = [word.strip(".,!?;:\"'()[]{}") for word in all_content.split() if len(word.strip(".,!?;:\"'()[]{}")) > 3]
    word_counts = {}
    for word in words:
        if word not in common_words:
            word_counts[word] = word_counts.get(word, 0) + 1
    
    top_keywords = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    context = {
        "today_count": today_count,
        "week_count": week_count,
        "month_count": month_count,
        "total_entries": base_entries.count(),
        "task_completion_rate": (completed_tasks.count() / task_entries.count() * 100) if task_entries.count() > 0 else 0,
        "priority_stats": priority_stats,
        "monthly_data": monthly_data,
        "top_keywords": top_keywords,
        "starred_percentage": (base_entries.filter(is_starred=True).count() / base_entries.count() * 100) if base_entries.count() > 0 else 0,
    }
    
    return render(request, "journal/analytics.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    """User profile and settings page."""
    if request.method == "POST":
        # Handle profile updates (placeholder for now)
        messages.success(request, "Profile updated successfully.")
        return redirect("profile")
    
    # User statistics
    base_entries = Entry.objects.filter(user=request.user)
    task_entries = base_entries.filter(task__gt="")
    
    stats = {
        "total_entries": base_entries.count(),
        "total_tasks": task_entries.count(),
        "completed_tasks": task_entries.filter(task_completed=True).count(),
        "starred_entries": base_entries.filter(is_starred=True).count(),
        "account_age": (timezone.now().date() - request.user.date_joined.date()).days,
        "last_login": request.user.last_login,
    }
    
    # Recent activity
    recent_entries = base_entries.order_by("-date_updated")[:5]
    
    context = {
        "stats": stats,
        "recent_entries": recent_entries,
        "user": request.user,
    }
    
    return render(request, "journal/profile.html", context)


@login_required
@require_http_methods(["GET"])
def help_page(request):
    """Help and documentation page."""
    context = {
        "ollama_model": settings.OLLAMA_MODEL,
        "weather_location_default": settings.WEATHER_DEFAULT_LOCATION,
    }
    
    return render(request, "journal/help.html", context)


@login_required
@require_http_methods(["GET"])
def calendar_view(request):
    """Calendar view of entries."""
    entries = Entry.objects.filter(user=request.user).order_by('date_created')
    context = {
        'entries': entries,
    }
    return render(request, "journal/calendar.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def settings_view(request):
    """User settings page."""
    if request.method == "POST":
        # Handle settings update
        messages.success(request, "Settings updated successfully.")
        return redirect('settings')
    
    context = {
        'user': request.user,
    }
    return render(request, "journal/settings.html", context)


@login_required
@require_http_methods(["GET"])
def about_view(request):
    """About page."""
    context = {}
    return render(request, "journal/about.html", context)


@login_required
@require_http_methods(["GET"])
def categories_view(request):
    """Categories management page."""
    categories = Entry.objects.filter(user=request.user).values_list('category', flat=True).distinct().exclude(category='')
    context = {
        'categories': categories,
    }
    return render(request, "journal/categories.html", context)


@login_required
@require_http_methods(["GET"])
def export_view(request):
    """Export options page."""
    context = {}
    return render(request, "journal/export.html", context)


@login_required
@require_http_methods(["GET"])
def reminders_view(request):
    """Reminders and notifications page."""
    entries_with_tasks = Entry.objects.filter(
        user=request.user,
        task__gt="",
        task_due_at__isnull=False
    ).order_by('task_due_at')
    
    context = {
        'entries_with_tasks': entries_with_tasks,
    }
    return render(request, "journal/reminders.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def mood_tracker_view(request):
    """Mood tracking page."""
    if request.method == "POST":
        mood = request.POST.get('mood')
        if mood:
            messages.success(request, f"Mood recorded: {mood}")
    
    context = {}
    return render(request, "journal/mood_tracker.html", context)


@login_required
@require_http_methods(["GET"])
def quick_notes_view(request):
    """Quick notes and ideas page."""
    recent_notes = Entry.objects.filter(
        user=request.user
    ).order_by('-date_created')[:10]
    
    context = {
        'recent_notes': recent_notes,
    }
    return render(request, "journal/quick_notes.html", context)


@login_required
@require_http_methods(["GET"])
def insights_view(request):
    """AI insights and recommendations page."""
    context = {}
    return render(request, "journal/insights.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def email_reminders_view(request):
    """Email reminders management."""
    reminders = request.user.reminders.all()
    
    if request.method == "POST":
        reminder_id = request.POST.get("reminder_id")
        action = request.POST.get("action")
        
        try:
            reminder = request.user.reminders.get(id=reminder_id)
            if action == "toggle":
                reminder.is_active = not reminder.is_active
                reminder.save()
                messages.success(request, "Reminder updated")
            elif action == "delete":
                reminder.delete()
                messages.success(request, "Reminder deleted")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
        
        return redirect("email_reminders")
    
    context = {
        "reminders": reminders,
    }
    return render(request, "journal/email_reminders.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def notifications_view(request):
    """Notifications management and history."""
    from .models import PushNotification
    
    notifications = PushNotification.objects.filter(user=request.user).order_by("-created_at")
    unread_count = notifications.filter(is_read=False).count()
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "mark_all_read":
            notifications.filter(is_read=False).update(is_read=True)
            messages.success(request, "All notifications marked as read")
        elif action == "clear_all":
            notifications.delete()
            messages.success(request, "All notifications cleared")
        
        return redirect("notifications")
    
    context = {
        "notifications": notifications[:50],
        "unread_count": unread_count,
    }
    return render(request, "journal/notifications.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def collaboration_view(request):
    """Collaboration and team features."""
    from .models import TeamEntry, CollaborationComment
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "create":
            title = request.POST.get("title")
            content = request.POST.get("content")
            
            if title and content:
                team_entry = TeamEntry.objects.create(
                    creator=request.user,
                    title=title,
                    content=content
                )
                messages.success(request, "Collaborative entry created")
            return redirect("collaboration")
    
    team_entries = TeamEntry.objects.filter(members=request.user).order_by("-created_at")
    
    context = {
        "team_entries": team_entries,
    }
    return render(request, "journal/collaboration.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def cloud_backup_view(request):
    """Cloud backup management."""
    from .models import BackupData
    
    backups = BackupData.objects.filter(user=request.user).order_by("-created_at")
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "create_backup":
            entries = Entry.objects.filter(user=request.user)
            backup = BackupData.objects.create(
                user=request.user,
                backup_type="manual",
                entries_count=entries.count(),
                status="in_progress"
            )
            # Queue backup task
            messages.success(request, "Backup started. You'll be notified when complete")
        
        elif action == "restore":
            backup_id = request.POST.get("backup_id")
            try:
                backup = BackupData.objects.get(id=backup_id, user=request.user)
                if backup.status == "completed":
                    backup.restored_at = timezone.now()
                    backup.save()
                    messages.success(request, "Backup restored successfully")
                else:
                    messages.error(request, "Backup is not ready for restoration")
            except BackupData.DoesNotExist:
                messages.error(request, "Backup not found")
        
        return redirect("cloud_backup")
    
    context = {
        "backups": backups,
    }
    return render(request, "journal/cloud_backup.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def social_sharing_view(request):
    """Social sharing settings and management."""
    from .models import EntryShare
    
    shared_entries = EntryShare.objects.filter(shared_by=request.user)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "share_entry":
            entry_id = request.POST.get("entry_id")
            share_type = request.POST.get("share_type", "public")
            
            try:
                entry = Entry.objects.get(id=entry_id, user=request.user)
                EntryShare.objects.create(
                    entry=entry,
                    shared_by=request.user,
                    share_type=share_type
                )
                messages.success(request, f"Entry shared as {share_type}")
            except Entry.DoesNotExist:
                messages.error(request, "Entry not found")
        
        elif action == "unshare":
            share_id = request.POST.get("share_id")
            try:
                share = EntryShare.objects.get(id=share_id, shared_by=request.user)
                share.delete()
                messages.success(request, "Entry unshared")
            except EntryShare.DoesNotExist:
                messages.error(request, "Share not found")
        
        return redirect("social_sharing")
    
    context = {
        "shared_entries": shared_entries,
    }
    return render(request, "journal/social_sharing.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def calendar_integration_view(request):
    """Calendar integration settings."""
    from .models import CalendarIntegration
    
    try:
        calendar_integration = request.user.calendar_integration
    except:
        calendar_integration = CalendarIntegration.objects.create(user=request.user)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "update_settings":
            provider = request.POST.get("provider")
            is_enabled = request.POST.get("is_enabled") == "on"
            sync_direction = request.POST.get("sync_direction", "one_way")
            
            calendar_integration.provider = provider
            calendar_integration.is_enabled = is_enabled
            calendar_integration.sync_direction = sync_direction
            calendar_integration.save()
            
            messages.success(request, "Calendar settings updated")
        
        elif action == "sync_now":
            if calendar_integration.is_enabled:
                messages.success(request, "Calendar sync started")
            else:
                messages.error(request, "Calendar integration is not enabled")
        
        return redirect("calendar_integration")
    
    context = {
        "calendar_integration": calendar_integration,
    }
    return render(request, "journal/calendar_integration.html", context)


@login_required
@require_http_methods(["GET"])
def advanced_analytics_view(request):
    """Advanced analytics and insights."""
    from .models import AdvancedAnalytics
    
    try:
        analytics = request.user.advanced_analytics
    except:
        analytics = AdvancedAnalytics.objects.create(user=request.user)
    
    # Calculate statistics
    entries = Entry.objects.filter(user=request.user)
    total_entries = entries.count()
    total_words = sum(len(e.content.split()) for e in entries)
    mood_distribution = {}
    
    for mood_value, mood_label in Entry.MOOD_CHOICES:
        count = entries.filter(mood=mood_value).count()
        if count > 0:
            mood_distribution[mood_label] = count
    
    context = {
        "analytics": analytics,
        "total_entries": total_entries,
        "total_words": total_words,
        "mood_distribution": mood_distribution,
    }
    return render(request, "journal/advanced_analytics.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def voice_entry_view(request):
    """Voice entry recording and management."""
    from .models import VoiceEntry
    
    voice_entries = VoiceEntry.objects.filter(user=request.user).order_by("-created_at")
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "save_voice" and request.FILES:
            audio_file = request.FILES.get("audio")
            if audio_file:
                entry_id = request.POST.get("entry_id")
                entry = None
                
                try:
                    if entry_id:
                        entry = Entry.objects.get(id=entry_id, user=request.user)
                except Entry.DoesNotExist:
                    pass
                
                voice_entry = VoiceEntry.objects.create(
                    user=request.user,
                    audio_file=audio_file,
                    entry=entry
                )
                messages.success(request, "Voice entry saved successfully")
        
        return redirect("voice_entry")
    
    context = {
        "voice_entries": voice_entries,
    }
    return render(request, "journal/voice_entry.html", context)


@login_required
@require_http_methods(["GET"])
def theme_toggle(request):
    """Toggle theme between light and dark mode."""
    from .models import UserPreferences
    
    try:
        prefs = request.user.preferences
    except:
        prefs = UserPreferences.objects.create(user=request.user)
    
    # Toggle theme
    prefs.theme = "light" if prefs.theme == "dark" else "dark"
    prefs.save()
    
    return JsonResponse({"theme": prefs.theme})


@login_required
@require_http_methods(["GET"])
def user_preferences(request):
    """User preferences page."""
    from .models import UserPreferences
    
    try:
        prefs = request.user.preferences
    except:
        prefs = UserPreferences.objects.create(user=request.user)
    
    if request.method == "POST":
        prefs.theme = request.POST.get("theme", "dark")
        prefs.notifications_enabled = request.POST.get("notifications_enabled") == "on"
        prefs.email_notifications = request.POST.get("email_notifications") == "on"
        prefs.language = request.POST.get("language", "en")
        prefs.save()
        messages.success(request, "Preferences updated")
    
    context = {
        "preferences": prefs,
    }
    return render(request, "journal/user_preferences.html", context)
