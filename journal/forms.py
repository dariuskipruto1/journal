from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
import logging

from .models import DocumentUpload, Entry, Tag, Reminder, UserPreferences

User = get_user_model()
logger = logging.getLogger(__name__)


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ["username", "email", "password1", "password2", "first_name", "last_name"]:
            self.fields[field_name].widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": self.fields[field_name].label,
                }
            )
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email


class EntryForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Entry
        fields = [
            "title",
            "category",
            "tags",
            "is_starred",
            "mood",
            "location",
            "task",
            "task_priority",
            "task_due_at",
            "task_completed",
            "alert_phone_number",
            "is_private",
            "content",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Entry title",
                    "maxlength": 200,
                }
            ),
            "category": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Personal, Work, Ideas...",
                    "maxlength": 100,
                    "list": "categories",
                }
            ),
            "is_starred": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "mood": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Where are you?",
                    "maxlength": 255,
                }
            ),
            "task": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional task label",
                    "maxlength": 100,
                }
            ),
            "task_priority": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "task_due_at": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "task_completed": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "is_private": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "alert_phone_number": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "+15551234567 (for WhatsApp alert)",
                    "maxlength": 32,
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 8,
                    "placeholder": "Capture your thoughts, progress, and next steps...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields["tags"].queryset = Tag.objects.filter(user=user)

        self.fields["is_starred"].required = False
        self.fields["task_due_at"].required = False
        self.fields["task_priority"].required = False
        self.fields["task_completed"].required = False
        self.fields["alert_phone_number"].required = False
        self.fields["is_private"].required = False
        self.fields["task_priority"].choices = [
            ("", "No priority"),
            *Entry.TASK_PRIORITY_CHOICES,
        ]
        self.fields["mood"].choices = [("", "No mood")] + list(Entry.MOOD_CHOICES)

        if self.instance and self.instance.pk and self.instance.task_due_at:
            local_due = timezone.localtime(self.instance.task_due_at)
            self.initial["task_due_at"] = local_due.strftime("%Y-%m-%dT%H:%M")

    def clean_title(self):
        title = (self.cleaned_data.get("title") or "").strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters long.")
        if len(title) > 200:
            raise forms.ValidationError("Title must not exceed 200 characters.")
        return title

    def clean_task(self):
        return (self.cleaned_data.get("task") or "").strip()

    def clean_task_due_at(self):
        task_due_at = self.cleaned_data.get("task_due_at")
        if task_due_at and timezone.is_naive(task_due_at):
            task_due_at = timezone.make_aware(task_due_at, timezone.get_current_timezone())
        return task_due_at

    def clean_content(self):
        content = (self.cleaned_data.get("content") or "").strip()
        if not content:
            raise forms.ValidationError("Content is required.")
        if len(content) < 5:
            raise forms.ValidationError("Content must be at least 5 characters long.")
        if len(content) > 50000:
            raise forms.ValidationError("Content must not exceed 50,000 characters.")
        return content

    def clean_alert_phone_number(self):
        phone = (self.cleaned_data.get("alert_phone_number") or "").strip()
        if not phone:
            return ""
        valid_chars = set("+0123456789")
        if any(char not in valid_chars for char in phone):
            raise forms.ValidationError(
                "Use international format digits only, for example +15551234567."
            )
        if not phone.startswith("+"):
            raise forms.ValidationError("Phone number must start with + and country code.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        task = (cleaned_data.get("task") or "").strip()
        task_priority = cleaned_data.get("task_priority")
        task_due_at = cleaned_data.get("task_due_at")
        task_completed = cleaned_data.get("task_completed")
        alert_phone_number = cleaned_data.get("alert_phone_number")

        if task_due_at and not task:
            self.add_error("task", "Add a task label before setting a due date.")

        if task_completed and not task:
            self.add_error("task", "Add a task label before marking a task complete.")

        if alert_phone_number and not task:
            self.add_error("task", "Add a task label before adding a WhatsApp alert number.")

        if task_priority and not task:
            self.add_error("task", "Add a task label before setting task priority.")

        if not task:
            cleaned_data["task_priority"] = ""
            cleaned_data["task_completed"] = False
            cleaned_data["task_due_at"] = None
            cleaned_data["alert_phone_number"] = ""

        return cleaned_data


class UploadForm(forms.ModelForm):
    class Meta:
        model = DocumentUpload
        fields = ["title", "file"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Add a descriptive title (optional)",
                    "maxlength": 200,
                }
            ),
            "file": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".pdf,.txt,.md,.csv,.mp4,.mov,.avi,.mkv,.jpg,.jpeg,.png,.gif",
                }
            ),
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get("file")
        if not uploaded_file:
            raise forms.ValidationError("Please upload a document or media file.")
        if uploaded_file.size > 150 * 1024 * 1024:
            raise forms.ValidationError("File size must be under 150MB.")
        return uploaded_file


class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ["reminder_time", "frequency", "is_active"]
        widgets = {
            "reminder_time": forms.DateTimeInput(
                attrs={
                    "class": "form-control",
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),
            "frequency": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "color"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tag name",
                    "maxlength": 50,
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "type": "color",
                }
            ),
        }


class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = [
            "theme",
            "notifications_enabled",
            "email_notifications",
            "sms_notifications",
            "language",
            "items_per_page",
            "show_analytics",
            "auto_save_draft",
        ]
        widgets = {
            "theme": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "notifications_enabled": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "email_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "sms_notifications": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "language": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),
            "items_per_page": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 5,
                    "max": 50,
                }
            ),
            "show_analytics": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "auto_save_draft": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

