from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.conf import settings
from datetime import datetime, timedelta

def create_calendar_event(appointment):
    """
    Crée un événement Google Calendar pour un rendez-vous.
    """
    # 🔑 Service Account JSON sur Render
    credentials = service_account.Credentials.from_service_account_file(
        "/etc/secrets/service_account.json",
        scopes=['https://www.googleapis.com/auth/calendar']
    )

    service = build('calendar', 'v3', credentials=credentials)

    # 🔹 Convertir date + time en datetime
    start_dt = datetime.combine(appointment.date, appointment.time)
    end_dt = start_dt + timedelta(hours=1)  # Durée 1 heure

    start_iso = start_dt.isoformat()
    end_iso = end_dt.isoformat()

    event = {
        'summary': f"Rendez-vous – {appointment.name}",
        'description': f"Projet: {appointment.project_type}\nNom: {appointment.name}\nEmail: {appointment.email}",
        'start': {
            'dateTime': start_iso,
            'timeZone': settings.GOOGLE_TIMEZONE,
        },
        'end': {
            'dateTime': end_iso,
            'timeZone': settings.GOOGLE_TIMEZONE,
        },
    }

    created_event = service.events().insert(
        calendarId=settings.GOOGLE_CALENDAR_ID,
        body=event
    ).execute()

    return created_event['id']
