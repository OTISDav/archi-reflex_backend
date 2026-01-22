from rest_framework import generics, permissions
from .models import Appointment
from .serializers import PublicAppointmentSerializer, AdminAppointmentSerializer
from core.google_calendar import create_calendar_event
from core.emails import send_notification
from django.conf import settings


class AppointmentAdminAPIView(generics.ListAPIView, generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AdminAppointmentSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"

    def perform_update(self, serializer):
        appointment = serializer.save()  # 🔹 Save met à jour directement

        new_status = serializer.validated_data.get("status")

        if new_status == "accepted":
            try:
                event_id = create_calendar_event(appointment)
                appointment.google_event_id = event_id
                appointment.save()
            except Exception as e:
                print(f"Erreur Google Calendar : {e}")

            send_notification(
                "Rendez-vous confirmé",
                f"Bonjour {appointment.name},\nVotre rendez-vous est confirmé.",
                appointment.email
            )

        elif new_status == "rejected":
            send_notification(
                "Rendez-vous refusé",
                f"Bonjour {appointment.name},\nVotre rendez-vous a été refusé.",
                appointment.email
            )
