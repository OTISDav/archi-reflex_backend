from celery import shared_task
from appointments.models import Appointment
from core.emails import send_notification
from core.google_calendar import create_calendar_event

@shared_task
def send_email_task(subject, message, recipient):
    try:
        send_notification(subject, message, recipient)
    except Exception as e:
        print(f"Erreur email async: {e}")


@shared_task
def create_calendar_event_task(appointment_id, delete=False):
    try:
        from .models import Appointment
        appointment = Appointment.objects.get(id=appointment_id)
        if delete and appointment.google_event_id:
            # supprime l'événement Google Calendar
            create_calendar_event(appointment, delete=True)
        elif not delete:
            # crée l'événement
            event_id = create_calendar_event(appointment)
            appointment.google_event_id = event_id
            appointment.save()
    except Exception as e:
        print(f"Erreur Google Calendar async: {e}")
