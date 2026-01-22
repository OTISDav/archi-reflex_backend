from rest_framework.views import APIView
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Appointment
from .serializers import AppointmentSerializer
from core.google_calendar import create_calendar_event
from core.emails import send_notification


# =========================
# CLIENT — CRÉATION RDV
# =========================
class AppointmentCreateAPIView(APIView):

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            # ⏳ RDV créé en attente
            appointment = serializer.save(status="pending")

            # 📧 Email ADMIN uniquement
            try:
                send_notification(
                    subject="Nouveau rendez-vous",
                    message=(
                        f"Nouveau RDV avec {appointment.name}\n"
                        f"Email : {appointment.email}\n"
                        f"Téléphone : {appointment.phone}"
                    ),
                    recipient=settings.ADMIN_EMAIL
                )
            except Exception as e:
                print(f"Erreur email admin: {e}")

            return Response(
                AppointmentSerializer(appointment).data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =========================
# ADMIN — GESTION RDV
# =========================
class AppointmentAdminAPIView(generics.GenericAPIView):

    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
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

        # =========================
        # LOGIQUE MÉTIER
        # =========================
        if old_status != new_status:
            try:
                # ✅ ACCEPTÉ
                if new_status == "accepted":

                    # 📅 Google Calendar (une seule fois)
                    if not appointment.google_event_id:
                        event_id = create_calendar_event(appointment)
                        appointment.google_event_id = event_id
                        appointment.save()

                    # 📧 Email confirmation client
                    send_notification(
                        subject="Votre rendez-vous est confirmé",
                        message=(
                            f"Bonjour {appointment.name},\n\n"
                            f"Votre RDV pour '{appointment.project_type}' "
                            f"a été confirmé.\n\n"
                            f"À très bientôt."
                        ),
                        recipient=appointment.email
                    )

                # ❌ REJETÉ
                elif new_status == "rejected":
                    send_notification(
                        subject="Votre rendez-vous a été annulé",
                        message=(
                            f"Bonjour {appointment.name},\n\n"
                            f"Votre RDV pour '{appointment.project_type}' "
                            f"a été annulé.\n\n"
                            f"Merci pour votre compréhension."
                        ),
                        recipient=appointment.email
                    )

            except Exception as e:
                print(f"Erreur notification RDV: {e}")

        return Response(serializer.data, status=status.HTTP_200_OK)
