from rest_framework.views import APIView
from django.conf import settings
from .models import Appointment
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from core.google_calendar import create_calendar_event
from core.emails import send_notification


# --- PUBLIC ---
class AppointmentCreateAPIView(APIView):
    """Permet au public de créer un rendez-vous"""

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()

            # Google Calendar
            try:
                event_id = create_calendar_event(appointment)
                appointment.google_event_id = event_id
                appointment.save()
            except Exception as e:
                print(f"Erreur Google Calendar: {e}")

            # Emails
            try:
                send_notification(
                    "Confirmation de rendez-vous",
                    f"Bonjour {appointment.name},\nVotre RDV pour '{appointment.project_type}' a bien été enregistré.",
                    appointment.email
                )
                send_notification(
                    "Nouveau rendez-vous",
                    f"Nouveau RDV avec {appointment.name} ({appointment.email}, {appointment.phone})",
                    settings.ADMIN_EMAIL
                )
            except Exception as e:
                print(f"Erreur envoi email: {e}")

            response_data = serializer.data
            response_data['google_event_id'] = appointment.google_event_id
            response_data['status'] = appointment.status
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --- ADMIN ---



class AppointmentAdminAPIView(generics.GenericAPIView):
    """
    Admin : lister tous les RDV et modifier leur statut
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        appointments = self.get_queryset()
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        appointment = self.get_object()
        serializer = self.get_serializer(
            appointment,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

