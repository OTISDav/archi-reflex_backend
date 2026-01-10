from rest_framework import generics
from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError
from cloudinary.uploader import upload
import os, time
from .models import Project
from .serializers import ProjectSerializer

class ProjectListAPIView(generics.ListAPIView):
    queryset = Project.objects.all().order_by('-year')
    serializer_class = ProjectSerializer
    permission_classes = []




class ProjectAdminAPIView(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)


    def perform_create(self, serializer):
        image = self.request.FILES.get("image")
        if not image:
            raise ValidationError({"image": "Aucune image reçue."})

        public_id = f"projects/{self.request.user.id}_{int(time.time())}"

        result = upload(image, resource_type="image", public_id=public_id, access_mode="public")

        file_url = result.get("secure_url")

        if not file_url:
            raise ValidationError({"image": "Échec de l'envoi sur Cloudinary."})

        serializer.save(image=file_url)

