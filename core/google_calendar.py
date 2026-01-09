from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.conf import settings

def create_calendar_event(appointment):
    """
    Crée un événement Google Calendar pour un rendez-vous
    """
    # Utiliser le fichier secret sur Render
    credentials = service_account.Credentials.from_service_account_file(
        "/etc/secrets/service_account.json",
        scopes=['https://www.googleapis.com/auth/calendar']
    )

    service = build('calendar', 'v3', credentials=credentials)

    start_datetime = f"{appointment.date}T{appointment.time}"

    event = {
        'summary': f"Rendez-vous – {appointment.name}",
        'description': appointment.message,
        'start': {
            'dateTime': start_datetime,
            'timeZone': settings.GOOGLE_TIMEZONE,
        },
        'end': {
            'dateTime': start_datetime,
            'timeZone': settings.GOOGLE_TIMEZONE,
        },
    }

    created_event = service.events().insert(
        calendarId=settings.GOOGLE_CALENDAR_ID,
        body=event
    ).execute()

    return created_event['id']
