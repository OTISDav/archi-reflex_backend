from rest_framework import generics, permissions
from .models import Appointment
from .serializers import PublicAppointmentSerializer, AdminAppointmentSerializer
from core.google_calendar import create_calendar_event
from core.emails import send_notification
from django.conf import settings


class AppointmentCreateAPIView(generics.CreateAPIView):
    """
    API publique : création d'un rendez-vous (status = pending)
    """
    queryset = Appointment.objects.all()
    serializer_class = PublicAppointmentSerializer
    permission_classes = []

    def perform_create(self, serializer):
        appointment = serializer.save(status="pending")

        # Email client
        send_notification(
            "Demande de rendez-vous reçue",
            f"Bonjour {appointment.name},\nVotre demande est en attente de confirmation.",
            appointment.email
        )

        # Email admin
        send_notification(
            "Nouveau rendez-vous en attente",
            f"{appointment.name} - {appointment.email} - {appointment.phone}",
            settings.ADMIN_EMAIL
        )


class AppointmentAdminAPIView(generics.ListAPIView, generics.UpdateAPIView):
    """
    API admin : liste + accepter / refuser un rendez-vous
    """
    queryset = Appointment.objects.all()
    serializer_class = AdminAppointmentSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"

    def perform_update(self, serializer):
        appointment = self.get_object()
        old_status = appointment.status
        new_status = serializer.validated_data.get("status")

        # Sécurité : pas de changement inutile
        if old_status == new_status:
            return

        serializer.save()

        if new_status == "accepted":
            # Google Calendar
            try:
                event_id = create_calendar_event(appointment)
                appointment.google_event_id = event_id
                appointment.save()
            except Exception as e:
                print(f"Erreur Google Calendar : {e}")

            # Email client
            send_notification(
                "Rendez-vous confirmé",
                f"Bonjour {appointment.name},\nVotre rendez-vous est confirmé.",
                appointment.email
            )

        elif new_status == "rejected":
            # Email client
            send_notification(
                "Rendez-vous refusé",
                f"Bonjour {appointment.name},\nVotre rendez-vous a été refusé.",
                appointment.email
            )
