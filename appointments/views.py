from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import PublicAppointmentSerializer, AdminAppointmentSerializer
from core.google_calendar import create_calendar_event
from core.emails import send_notification
from django.conf import settings

class AppointmentCreateAPIView(generics.CreateAPIView):
    """
    API publique : le client crée un RDV → status = pending
    """
    queryset = Appointment.objects.all()
    serializer_class = PublicAppointmentSerializer
    permission_classes = []  # ouvert au public

    def perform_create(self, serializer):
        appointment = serializer.save(status="pending")

        # Email client et admin
        try:
            send_notification(
                "Confirmation de réception du rendez-vous",
                f"Bonjour {appointment.name},\nVotre RDV pour '{appointment.project_type}' a bien été enregistré et est en attente de confirmation.",
                appointment.email
            )
            send_notification(
                "Nouveau rendez-vous",
                f"Nouveau RDV avec {appointment.name} ({appointment.email}, {appointment.phone})",
                settings.ADMIN_EMAIL
            )
        except Exception as e:
            import logging
            logging.error(f"Erreur envoi email: {e}")

class AppointmentAdminAPIView(generics.GenericAPIView):
    """
    API admin : consulter et mettre à jour le statut d'un RDV
    """
    queryset = Appointment.objects.all()
    serializer_class = AdminAppointmentSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"

    def get(self, request, pk=None):
        if pk:
            appointment = self.get_object()
            serializer = self.get_serializer(appointment)
        else:
            appointments = self.get_queryset()
            serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        appointment = self.get_object()
        old_status = appointment.status

        serializer = self.get_serializer(
            appointment,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_status = serializer.instance.status

        # 🔔 Actions uniquement si le status change
        if old_status != new_status:
            try:
                if new_status == "accepted":
                    # Créer événement Google Calendar
                    try:
                        event_id = create_calendar_event(appointment)
                        appointment.google_event_id = event_id
                        appointment.save()
                    except Exception as e:
                        import logging
                        logging.error(f"Erreur Google Calendar: {e}")

                    # Email confirmation client
                    send_notification(
                        "Votre rendez-vous est confirmé",
                        f"Bonjour {appointment.name},\nVotre RDV pour '{appointment.project_type}' a été confirmé.",
                        appointment.email
                    )

                elif new_status == "rejected":
                    # Email annulation client
                    send_notification(
                        "Votre rendez-vous a été annulé",
                        f"Bonjour {appointment.name},\nVotre RDV pour '{appointment.project_type}' a été annulé.",
                        appointment.email
                    )
            except Exception as e:
                import logging
                logging.error(f"Erreur envoi email notification status: {e}")

        return Response(serializer.data, status=status.HTTP_200_OK)
