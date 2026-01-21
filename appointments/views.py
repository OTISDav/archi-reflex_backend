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
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            # Création du RDV avec statut pending
            appointment = serializer.save(status="pending")

            # 📧 Notification admin uniquement
            try:
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
            except Exception as e:
                print(f"Erreur email admin: {e}")

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ==========================
# 🔹 Admin RDV (Liste / Détail / Confirmation)
# ==========================
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


    # ✏️ Mise à jour (confirmation / annulation)
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

        # ==========================
        # ✅ Confirmation du RDV
        # ==========================
        if old_status != "confirmed" and new_status == "confirmed":

            # 📅 Création Google Calendar
            try:
                event_id = create_calendar_event(appointment)
                appointment.google_event_id = event_id
                appointment.save()
            except Exception as e:
                print(f"Erreur Google Calendar: {e}")

            # 📧 Email client confirmation
            try:
                send_notification(
                    subject="Votre rendez-vous est confirmé ✅",
                    message=(
                        f"Bonjour {appointment.name},\n\n"
                        f"Votre rendez-vous pour le projet "
                        f"\"{appointment.project_type}\" a été confirmé.\n\n"
                        f"📅 Date : {appointment.date}\n"
                        f"⏰ Heure : {appointment.time}\n\n"
                        f"À très bientôt."
                    ),
                    recipient=appointment.email
                )
            except Exception as e:
                print(f"Erreur email confirmation: {e}")

        # ==========================
        # ❌ Annulation du RDV
        # ==========================
        elif old_status != "cancelled" and new_status == "cancelled":
            try:
                send_notification(
                    subject="Rendez-vous annulé ❌",
                    message=(
                        f"Bonjour {appointment.name},\n\n"
                        f"Votre rendez-vous pour le projet "
                        f"\"{appointment.project_type}\" a été annulé."
                    ),
                    recipient=appointment.email
                )
            except Exception as e:
                print(f"Erreur email annulation: {e}")

        return Response(serializer.data, status=status.HTTP_200_OK)
