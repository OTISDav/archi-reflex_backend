from rest_framework.views import APIView
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Appointment
from .serializers import AppointmentSerializer
from core.google_calendar import create_calendar_event
from core.emails import send_notification


# ==========================
# 🔹 Création RDV (Client)
# ==========================
class AppointmentCreateAPIView(APIView):

    def post(self, request):
        serializer = AppointmentSerializer(
            data=request.data,
            context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        appointment = serializer.save(status="pending")

        send_notification(
            subject="Nouvelle demande de rendez-vous",
            message=(
                f"Nouveau rendez-vous demandé\n\n"
                f"Nom : {appointment.name}\n"
                f"Email : {appointment.email}\n"
                f"Téléphone : {appointment.phone}\n"
                f"Projet : {appointment.project_type}\n"
                f"Date : {appointment.date} à {appointment.time}"
            ),
            recipient=settings.ADMIN_EMAIL
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ==========================
# 🔹 Admin RDV
# ==========================
class AppointmentAdminAPIView(generics.GenericAPIView):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"

    def patch(self, request, pk):
        appointment = self.get_object()
        old_status = appointment.status
        new_status = request.data.get("status")

        # 🔒 Sécurité transitions
        if old_status == "confirmed" and new_status == "confirmed":
            return Response(
                {"detail": "Rendez-vous déjà confirmé."},
                status=status.HTTP_409_CONFLICT
            )

        if old_status == "cancelled":
            return Response(
                {"detail": "Impossible de modifier un rendez-vous annulé."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ==========================
        # ✅ CONFIRMATION
        # ==========================
        if old_status == "pending" and new_status == "confirmed":

            # 📅 Google Calendar (une seule fois)
            if not appointment.google_event_id:
                event_id = create_calendar_event(appointment)
                appointment.google_event_id = event_id

            # 📧 Email client
            send_notification(
                subject="Votre rendez-vous est confirmé ✅",
                message=(
                    f"Bonjour {appointment.name},\n\n"
                    f"Votre rendez-vous pour le projet "
                    f"\"{appointment.project_type}\" est confirmé.\n\n"
                    f"📅 Date : {appointment.date}\n"
                    f"⏰ Heure : {appointment.time}\n\n"
                    f"À très bientôt."
                ),
                recipient=appointment.email
            )

            appointment.status = "confirmed"
            appointment.save()

        # ==========================
        # ❌ ANNULATION
        # ==========================
        elif new_status == "cancelled":
            appointment.status = "cancelled"
            appointment.save()

            send_notification(
                subject="Rendez-vous annulé ❌",
                message=(
                    f"Bonjour {appointment.name},\n\n"
                    f"Votre rendez-vous a été annulé."
                ),
                recipient=appointment.email
            )

        # Serializer uniquement pour la réponse
        serializer = AppointmentSerializer(
            appointment,
            context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
