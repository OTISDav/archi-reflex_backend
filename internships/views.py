from rest_framework.views import APIView
from django.conf import settings
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Internship
from .serializers import InternshipSerializer

from core.emails import send_notification

# --- PUBLIC ---
class InternshipCreateAPIView(APIView):
    """Soumettre une demande de stage"""
    def post(self, request):
        serializer = InternshipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        internship = serializer.save()

        # Emails
        try:
            send_notification(
                "Confirmation de candidature",
                f"Bonjour {internship.name},\nVotre demande de stage a bien été enregistrée.",
                internship.email
            )
            send_notification(
                "Nouvelle demande de stage",
                f"{internship.name} ({internship.email}, {internship.phone}) a postulé",
                settings.ADMIN_EMAIL
            )
        except Exception as e:
            print(f"Erreur envoi email: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

# --- ADMIN ---


class InternshipAdminAPIView(generics.GenericAPIView):
    """Admin : voir et gérer toutes les demandes de stage"""
    queryset = Internship.objects.all().order_by('-created_at')
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        internships = self.get_queryset()
        serializer = self.get_serializer(internships, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        internship = self.get_object()
        serializer = self.get_serializer(
            internship,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

