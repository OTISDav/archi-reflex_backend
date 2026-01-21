# appointments/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Appointment
from core.google_calendar import create_calendar_event
from core.emails import send_notification

@receiver(post_save, sender=Appointment)
def appointment_status_handler(sender, instance, created, **kwargs):
    # Ne rien faire à la création (handled côté create API)
    if created:
        return

    # Si le statut a changé
    if 'status' in instance.__dict__:  # sécurité
        if instance.status == "confirmed":
            # Google Calendar
            if not instance.google_event_id:
                try:
                    event_id = create_calendar_event(instance)
                    instance.google_event_id = event_id
                    instance.save()
                except Exception as e:
                    print(f"Erreur Google Calendar signal: {e}")

            # Email au client
            try:
                send_notification(
                    subject="Votre rendez-vous est confirmé ✅",
                    message=(
                        f"Bonjour {instance.name},\nVotre rendez-vous pour '{instance.project_type}' a été confirmé.\n"
                        f"📅 Date: {instance.date}\n⏰ Heure: {instance.time}"
                    ),
                    recipient=instance.email
                )
            except Exception as e:
                print(f"Erreur email confirmation signal: {e}")

        elif instance.status == "cancelled":
            # Email annulation
            try:
                send_notification(
                    subject="Rendez-vous annulé ❌",
                    message=f"Bonjour {instance.name},\nVotre rendez-vous pour '{instance.project_type}' a été annulé.",
                    recipient=instance.email
                )
            except Exception as e:
                print(f"Erreur email annulation signal: {e}")
