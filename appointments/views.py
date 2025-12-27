from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
from .serializers import AppointmentSerializer
from core.google_calendar import create_calendar_event
from core.emails import send_notification


class AppointmentCreateAPIView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            # Création du rendez-vous dans la base
            appointment = serializer.save()

            # --- Google Calendar ---
            try:
                event_id = create_calendar_event(appointment)
                appointment.google_event_id = event_id
                appointment.save()
            except Exception as e:
                print(f"Erreur Google Calendar: {e}")

            # --- Emails ---
            try:
                # Email client
                send_notification(
                    "Confirmation de rendez-vous",
                    f"Bonjour {appointment.name},\n\nVotre rendez-vous pour '{appointment.project_type}' a bien été enregistré.\n\nMerci.",
                    appointment.email
                )

                # Email admin
                send_notification(
                    "Nouveau rendez-vous",
                    f"Nouveau RDV avec {appointment.name} ({appointment.email}, {appointment.phone})",
                    settings.ADMIN_EMAIL
                )
            except Exception as e:
                print(f"Erreur envoi email: {e}")

            # --- Préparer la réponse ---
            response_data = serializer.data
            response_data['google_event_id'] = appointment.google_event_id
            response_data['status'] = appointment.status

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
