# Journal Desk

A personal journal and task management application built with Django. Write entries, manage tasks, get weather updates, and receive AI-powered recommendations.

## Features

- **Journal Entries**: Create, read, update, and delete journal entries
- **Task Management**: Add tasks to entries with due dates and priority levels
- **Entry Filtering**: Filter entries by status, priority, search terms, and sort options
- **Export**: Export journal entries to CSV format
- **User Authentication**: Secure user registration and login
- **Task Alerts**: Email and WhatsApp reminders for overdue tasks
- **AI Assistant**: Integration with Ollama for intelligent task recommendations
- **Weather Integration**: Real-time weather data in the AI responses
- **Starred Entries**: Mark favorite entries for quick access
- **Statistics Dashboard**: View summary stats about your journal

## Technology Stack

- **Backend**: Django 4.2
- **Database**: SQLite3
- **AI**: Ollama (local LLM)
- **Notifications**: Email, Twilio WhatsApp
- **Frontend**: HTML/CSS with Font Awesome icons

## Installation

### Prerequisites
- Python 3.8+
- Ollama (for AI features) - optional

### Setup

1. Clone the repository and navigate to the project:
```bash
cd /path/to/journal_project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment file:
```bash
cp .env.example .env
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (admin):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Configuration

### Environment Variables

Edit `.env` file to configure:

- `DJANGO_SECRET_KEY`: Secret key for Django (change in production)
- `DJANGO_DEBUG`: Set to False in production
- `DJANGO_ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Email Configuration

Configure email settings in `.env` to enable email alerts:
- `DJANGO_EMAIL_BACKEND`
- `DJANGO_EMAIL_HOST`
- `DJANGO_DEFAULT_FROM_EMAIL`

### WhatsApp Alerts (Optional)

Set up Twilio credentials to enable WhatsApp task reminders:
- `TASK_ALERTS_WHATSAPP_ENABLED=True`
- `WHATSAPP_PROVIDER=twilio`
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_WHATSAPP_FROM`

### Ollama AI Integration (Optional)

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama2`
3. Set in `.env`: `OLLAMA_BASE_URL=http://127.0.0.1:11434`

## Usage

### Creating an Entry

1. Click "Sign up" to create an account
2. Log in and navigate to the home page
3. Fill in the entry form:
   - **Title**: Entry headline (3-200 characters)
   - **Content**: Main text (10-50000 characters)
   - **Task** (optional): Task label
   - **Task Priority**: Low, Medium, High
   - **Due Date** (optional): When the task should be completed
   - **Starred**: Mark as favorite

### Managing Tasks

- Set a due date to create a deadline
- Check "Completed" to mark as done
- View overdue tasks in the alert box at the top
- Add a WhatsApp number to get alerts

### AI Assistant

Type in the chat to get AI-powered help. The AI understands:
- **Recommendations**: Suggest next steps based on your journal
- **Real-time**: Ask for current time and date
- **Weather**: Ask for current conditions
- **Journal context**: References your entries for personalized suggestions

### Exporting Data

Click "Export CSV" to download your filtered entries as a spreadsheet.

## Management Commands

### Send Task Alerts

Send overdue task reminders via email and WhatsApp:
```bash
python manage.py send_task_alerts
```

Schedule this to run periodically (e.g., via cron):
```
0 9 * * * cd /path/to/project && python manage.py send_task_alerts
```

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` with your superuser credentials to:
- Manage users
- View and edit entries
- Monitor system health

## Logging

Logs are automatically saved to `logs/journal.log`. In production, check logs for:
- Failed email delivery
- Ollama connection issues
- Form validation errors
- Database issues

## Security

The application includes:
- User authentication and authorization
- CSRF protection
- Secure password hashing
- Session management
- SQL injection prevention via ORM
- XSS protection
- HSTS headers (in production)

Default DEBUG=True for development. **Change to DEBUG=False before deploying to production**.

## Troubleshooting

### Ollama Not Connecting
- Ensure Ollama is running: `ollama serve`
- Check `OLLAMA_BASE_URL` in `.env`
- Check logs: `tail -f logs/journal.log`

### Email Not Sending
- Verify `DJANGO_EMAIL_BACKEND` is configured
- Check credentials in `.env`
- For Gmail, use an app-specific password
- Check logs for errors

### Database Locked
- Ensure only one instance of the app is running
- Use `python manage.py migrate` to fix migration issues
- Delete `db.sqlite3` to start fresh

### Port Already in Use
```bash
python manage.py runserver 8001  # Use a different port
```

## Development

### Running Tests

```bash
python manage.py test journal
```

### Code Style

The project follows Django conventions. Run checks:
```bash
python manage.py check
```

## Performance Tips

- Enable caching in `.env` for production
- Use `python manage.py collectstatic` for static files
- Monitor database queries in development: add `django-debug-toolbar`
- Use database connection pooling in production

## Deployment

For production deployment:

1. Set `DEBUG=False`
2. Generate a new `DJANGO_SECRET_KEY`
3. Use a production database (PostgreSQL recommended)
4. Use a production WSGI server (Gunicorn)
5. Set up SSL/TLS certificates
6. Configure `ALLOWED_HOSTS`
7. Use environment variables for sensitive data

Example production setup:
```bash
gunicorn journal_project.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests.

## Support

For issues, questions, or suggestions, please open an issue on the project repository.
