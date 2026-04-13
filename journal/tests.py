import json
from datetime import timedelta
from io import BytesIO
from unittest.mock import MagicMock, patch
from urllib import error as urllib_error

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import EntryForm

from .models import Entry

User = get_user_model()


class JournalViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alex", password="StrongPass123", email="alex@example.com"
        )
        self.other_user = User.objects.create_user(
            username="sam", password="StrongPass123", email="sam@example.com"
        )

    def test_entry_list_requires_login(self):
        response = self.client.get(reverse("entry_list"))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('entry_list')}"
        )

    def test_entry_list_shows_only_current_user_entries(self):
        Entry.objects.create(
            user=self.user,
            title="Personal note",
            content="This is a private entry visible only to alex.",
        )
        Entry.objects.create(
            user=self.other_user,
            title="Another note",
            content="This entry belongs to sam and should be hidden.",
        )

        self.client.login(username="alex", password="StrongPass123")
        response = self.client.get(reverse("entry_list"))

        self.assertContains(response, "Personal note")
        self.assertNotContains(response, "Another note")

    def test_post_entry_assigns_logged_in_user(self):
        self.client.login(username="alex", password="StrongPass123")

        response = self.client.post(
            reverse("entry_list"),
            {
                "title": "Sprint summary",
                "task": "planning",
                "task_due_at": "",
                "task_completed": "",
                "alert_phone_number": "",
                "content": "We completed our sprint goals and planned next actions.",
            },
        )

        self.assertRedirects(response, reverse("entry_list"))
        entry = Entry.objects.get(title="Sprint summary")
        self.assertEqual(entry.user, self.user)

    def test_toggle_task_status_marks_task_complete(self):
        self.client.login(username="alex", password="StrongPass123")
        entry = Entry.objects.create(
            user=self.user,
            title="Payment",
            task="Pay bill",
            task_due_at=timezone.now() + timedelta(hours=2),
            content="Need to pay utility bill today.",
        )

        response = self.client.post(
            reverse("entry_toggle_task", args=[entry.pk]),
            {"next": reverse("entry_list")},
        )

        self.assertRedirects(response, reverse("entry_list"))
        entry.refresh_from_db()
        self.assertTrue(entry.task_completed)

    def test_entry_is_overdue_property_works_when_due_date_passed(self):
        entry = Entry.objects.create(
            user=self.user,
            title="Overdue task",
            task="Check report",
            task_due_at=timezone.now() - timedelta(hours=2),
            content="This task is now overdue.",
        )

        self.assertTrue(entry.is_overdue)

    def test_entry_form_due_at_becomes_aware_time_zone(self):
        local_dt = timezone.localtime(timezone.now() + timedelta(hours=3))
        payload = {
            "title": "Timezone test",
            "task": "Timezone check",
            "task_due_at": local_dt.strftime("%Y-%m-%dT%H:%M"),
            "content": "Ensure due date timezone conversion works correctly.",
        }

        form = EntryForm(data=payload)
        self.assertTrue(form.is_valid(), form.errors.as_json())

        task_due_at = form.cleaned_data["task_due_at"]
        self.assertIsNotNone(task_due_at)
        self.assertTrue(timezone.is_aware(task_due_at))


class SignupTests(TestCase):
    def test_signup_creates_user_and_redirects(self):
        response = self.client.post(
            reverse("signup"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "VeryStrongPass123",
                "password2": "VeryStrongPass123",
            },
        )

        self.assertRedirects(response, reverse("entry_list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())


class TaskAlertCommandTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alerts", password="StrongPass123", email="alerts@example.com"
        )

    def test_send_task_alerts_marks_alert_sent(self):
        entry = Entry.objects.create(
            user=self.user,
            title="Late task",
            task="Submit tax form",
            task_due_at=timezone.now() - timedelta(hours=1),
            content="Need to submit before deadline.",
        )

        with patch(
            "journal.management.commands.send_task_alerts.send_overdue_task_alert",
            return_value={"email": True, "whatsapp": False},
        ) as mocked_alert:
            call_command("send_task_alerts")

        mocked_alert.assert_called_once()
        entry.refresh_from_db()
        self.assertIsNotNone(entry.alert_sent_at)

    def test_send_task_alerts_skips_completed_tasks(self):
        entry = Entry.objects.create(
            user=self.user,
            title="Done task",
            task="Book tickets",
            task_due_at=timezone.now() - timedelta(hours=2),
            task_completed=True,
            content="Task was already completed.",
        )

        with patch(
            "journal.management.commands.send_task_alerts.send_overdue_task_alert",
            return_value={"email": True, "whatsapp": False},
        ) as mocked_alert:
            call_command("send_task_alerts")

        mocked_alert.assert_not_called()
        entry.refresh_from_db()
        self.assertIsNone(entry.alert_sent_at)


class OllamaChatTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="assistant", password="StrongPass123", email="assistant@example.com"
        )

    def test_ollama_chat_requires_login(self):
        response = self.client.post(
            reverse("ollama_chat"),
            data=json.dumps({"prompt": "Hello"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 302)

    @patch("journal.views.urllib_request.urlopen")
    def test_ollama_chat_returns_reply(self, mocked_urlopen):
        self.client.login(username="assistant", password="StrongPass123")
        mocked_response = MagicMock()
        mocked_response.read.return_value = json.dumps(
            {"model": "llama3.2", "message": {"content": "Hi there!"}}
        ).encode("utf-8")
        mocked_urlopen.return_value.__enter__.return_value = mocked_response

        response = self.client.post(
            reverse("ollama_chat"),
            data=json.dumps({"prompt": "Hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200, response.content.decode("utf-8"))
        self.assertJSONEqual(
            response.content.decode("utf-8"),
            {"reply": "Hi there!", "model": "llama3.2"},
        )

    @patch("journal.views.urllib_request.urlopen")
    def test_ollama_chat_handles_connection_error(self, mocked_urlopen):
        self.client.login(username="assistant", password="StrongPass123")
        mocked_urlopen.side_effect = urllib_error.URLError("connection refused")

        response = self.client.post(
            reverse("ollama_chat"),
            data=json.dumps({"prompt": "Hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 502)
        self.assertIn("Could not connect to Ollama", response.json()["error"])

    @patch("journal.views.urllib_request.urlopen")
    def test_ollama_chat_falls_back_when_default_model_is_missing(self, mocked_urlopen):
        self.client.login(username="assistant", password="StrongPass123")

        missing_model_error = urllib_error.HTTPError(
            url="http://127.0.0.1:11434/api/chat",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=BytesIO(b'model "llama2" not found'),
        )

        tags_response = MagicMock()
        tags_response.read.return_value = json.dumps(
            {
                "models": [
                    {"name": "mistral:latest"},
                ]
            }
        ).encode("utf-8")
        tags_context = MagicMock()
        tags_context.__enter__.return_value = tags_response

        fallback_response = MagicMock()
        fallback_response.read.return_value = json.dumps(
            {"model": "mistral", "message": {"content": "Fallback model replied."}}
        ).encode("utf-8")
        fallback_context = MagicMock()
        fallback_context.__enter__.return_value = fallback_response

        mocked_urlopen.side_effect = [missing_model_error, tags_context, fallback_context]

        response = self.client.post(
            reverse("ollama_chat"),
            data=json.dumps({"prompt": "Hello"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200, response.content.decode("utf-8"))
        payload = response.json()
        self.assertEqual(payload["reply"], "Fallback model replied.")
        self.assertEqual(payload["model"], "mistral")
        self.assertIn("Using 'mistral' instead", payload.get("model_notice", ""))

    @patch("journal.views.urllib_request.urlopen")
    def test_ollama_chat_recommendations_include_journal_context(self, mocked_urlopen):
        self.client.login(username="assistant", password="StrongPass123")
        Entry.objects.create(
            user=self.user,
            title="Quarter goals",
            task="Plan roadmap",
            content="Need clear priorities for this quarter.",
        )
        mocked_response = MagicMock()
        mocked_response.read.return_value = json.dumps(
            {"model": "llama3.2", "message": {"content": "Focus on your roadmap first."}}
        ).encode("utf-8")
        mocked_urlopen.return_value.__enter__.return_value = mocked_response

        response = self.client.post(
            reverse("ollama_chat"),
            data=json.dumps({"prompt": "Recommend what I should do next"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        ollama_request = mocked_urlopen.call_args[0][0]
        ollama_payload = json.loads(ollama_request.data.decode("utf-8"))
        self.assertIn("Journal snapshot", ollama_payload["messages"][1]["content"])

    def test_assistant_realtime_returns_clock_data(self):
        self.client.login(username="assistant", password="StrongPass123")

        response = self.client.get(reverse("assistant_realtime"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("realtime", payload)
        self.assertIn("local_datetime", payload["realtime"])

    @patch("journal.views.urllib_request.urlopen")
    def test_assistant_realtime_returns_weather_when_location_given(self, mocked_urlopen):
        self.client.login(username="assistant", password="StrongPass123")

        geocode_response = MagicMock()
        geocode_response.read.return_value = json.dumps(
            {
                "results": [
                    {
                        "name": "Nairobi",
                        "admin1": "Nairobi County",
                        "country": "Kenya",
                        "latitude": -1.2833,
                        "longitude": 36.8167,
                    }
                ]
            }
        ).encode("utf-8")
        geocode_context = MagicMock()
        geocode_context.__enter__.return_value = geocode_response

        weather_response = MagicMock()
        weather_response.read.return_value = json.dumps(
            {
                "timezone": "Africa/Nairobi",
                "current": {
                    "time": "2026-04-03T14:00",
                    "temperature_2m": 24.2,
                    "apparent_temperature": 25.0,
                    "precipitation": 0.0,
                    "weather_code": 1,
                    "wind_speed_10m": 8.1,
                },
            }
        ).encode("utf-8")
        weather_context = MagicMock()
        weather_context.__enter__.return_value = weather_response

        mocked_urlopen.side_effect = [geocode_context, weather_context]

        response = self.client.get(reverse("assistant_realtime"), {"location": "Nairobi"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("weather", payload)
        self.assertEqual(payload["weather"]["location"], "Nairobi, Nairobi County, Kenya")
