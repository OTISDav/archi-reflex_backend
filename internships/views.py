from rest_framework.views import APIView
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.response import Response
from .models import Internship
from .serializers import InternshipSerializer
from cloudinary.uploader import upload
from rest_framework import generics, permissions
from django.core.exceptions import ValidationError
import time

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 Mo max par fichier

from core.emails import send_notification

class InternshipCreateAPIView(APIView):
    """Soumettre une demande de stage avec upload Cloudinary"""
    def post(self, request):
        cv = request.FILES.get("cv")
        letter = request.FILES.get("letter")

        if not cv or not letter:
            return Response({"detail": "CV et lettre sont requis."}, status=400)

        # Vérification taille
        if cv.size > MAX_FILE_SIZE:
            return Response({"cv": "Le CV est trop volumineux (max 10 Mo)."}, status=400)
        if letter.size > MAX_FILE_SIZE:
            return Response({"letter": "La lettre est trop volumineuse (max 10 Mo)."}, status=400)

        # Upload Cloudinary
        cv_result = upload(cv, resource_type="raw", public_id=f"internships/cv/{int(time.time())}_{cv.name}")
        letter_result = upload(letter, resource_type="raw", public_id=f"internships/letters/{int(time.time())}_{letter.name}")

        # Création de l'objet Internship
        serializer = InternshipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        internship = serializer.save(
            cv=cv_result.get("secure_url"),
            letter=letter_result.get("secure_url")
        )

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




class InternshipAdminAPIView(generics.GenericAPIView):
    """Admin : voir et gérer toutes les demandes de stage"""
    queryset = Internship.objects.all().order_by('-created_at')
    serializer_class = InternshipSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        internships = self.get_queryset()
        serializer = self.get_serializer(internships, many=True)
        return Response(serializer.data, status=200)

    def patch(self, request, pk):
        internship = self.get_object()
        serializer = self.get_serializer(
            internship,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)
