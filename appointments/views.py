from rest_framework.views import APIView
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from core.google_calendar import create_calendar_event
from core.emails import send_notification
import logging

logger = logging.getLogger(__name__)


# =========================
# Création RDV côté client
# =========================
class AppointmentCreateAPIView(APIView):

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            # Créer RDV en pending par défaut
            appointment = serializer.save(status="pending")

            # 🔔 Notification admin uniquement
            try:
                send_notification(
                    subject="Nouvelle demande de rendez-vous",
                    message=(
                        f"Nouveau RDV demandé\n\n"
                        f"Nom: {appointment.name}\n"
                        f"Email: {appointment.email}\n"
                        f"Téléphone: {appointment.phone}\n"
                        f"Projet: {appointment.project_type}\n"
                        f"Date: {appointment.date} {appointment.time}"
                    ),
                    recipient=settings.ADMIN_EMAIL
                )
            except Exception as e:
                logger.error("Erreur email admin lors création RDV", exc_info=True)

            response_data = serializer.data
            response_data['status'] = appointment.status
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# Admin RDV (Liste / Détail / Confirmation / Annulation)
# =========================
class AppointmentAdminAPIView(generics.GenericAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "pk"

    # 📄 Liste ou détail
    def get(self, request, pk=None):
        if pk:
            appointment = self.get_object()
            serializer = self.get_serializer(appointment)
        else:
            appointments = self.get_queryset()
            serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    # ✏️ Mise à jour status
    def patch(self, request, pk):
        appointment = self.get_object()
        old_status = appointment.status
        new_status = request.data.get("status")

        if new_status not in ["pending", "confirmed", "cancelled"]:
            return Response({"detail": "Status invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Mettre à jour tous les champs envoyés
        serializer = self.get_serializer(appointment, data=request.data, partial=True, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # =========================
        # ✅ Confirmation
        # =========================
        if old_status != "confirmed" and new_status == "confirmed":
            try:
                # Google Calendar
                if not appointment.google_event_id:
                    event_id = create_calendar_event(appointment)
                    appointment.google_event_id = event_id
                    appointment.save()

                # Email au client
                send_notification(
                    subject="Votre rendez-vous est confirmé ✅",
                    message=(
                        f"Bonjour {appointment.name},\n"
                        f"Votre RDV pour '{appointment.project_type}' a été confirmé.\n"
                        f"📅 Date: {appointment.date}\n⏰ Heure: {appointment.time}"
                    ),
                    recipient=appointment.email
                )
            except Exception as e:
                logger.error("Erreur confirmation RDV", exc_info=True)

        # =========================
        # ❌ Annulation
        # =========================
        elif old_status != "cancelled" and new_status == "cancelled":
            try:
                send_notification(
                    subject="Votre rendez-vous est annulé ❌",
                    message=(
                        f"Bonjour {appointment.name},\n"
                        f"Votre RDV pour '{appointment.project_type}' a été annulé."
                    ),
                    recipient=appointment.email
                )
            except Exception as e:
                logger.error("Erreur annulation RDV", exc_info=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
