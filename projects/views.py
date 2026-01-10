from rest_framework import generics, permissions, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Project
from .serializers import ProjectSerializer

# --- PUBLIC ---
class ProjectListAPIView(generics.ListAPIView):
    """Liste publique des projets"""
    queryset = Project.objects.all().order_by('-year')
    serializer_class = ProjectSerializer
    permission_classes = []  # Public


# --- ADMIN ---
# class ProjectAdminAPIView(viewsets.ModelViewSet):
#     """CRUD complet pour l'admin"""
#     queryset = Project.objects.all()
#     serializer_class = ProjectSerializer
#     permission_classes = [permissions.IsAdminUser]
#     parser_classes = (MultiPartParser, FormParser)  # Pour upload image


from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from cloudinary.uploader import upload
import os, time
from .models import Project
from .serializers import ProjectSerializer

class ProjectAdminAPIView(viewsets.ModelViewSet):
    """CRUD complet pour l'admin avec upload Cloudinary"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)  # pour recevoir les fichiers

    def perform_create(self, serializer):
        image = self.request.FILES.get("image")  # clé envoyée depuis frontend

        if not image:
            raise ValidationError({"image": "Aucune image reçue."})

        # Générer un nom unique pour l'image
        filename_base = f"{self.request.user.id}_{int(time.time())}"
        public_id = f"projects/{filename_base}"

        # Upload sur Cloudinary
        result = upload(image, resource_type="image", public_id=public_id, access_mode="public")
        file_url = result.get("secure_url")

        if not file_url:
            raise ValidationError({"image": "Échec de l'envoi sur Cloudinary."})

        # Sauvegarde de l'objet Project avec l'URL Cloudinary
        serializer.save(image=file_url)
