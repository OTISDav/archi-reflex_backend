from rest_framework import generics, permissions, viewsets
from .models import Project
from .serializers import ProjectSerializer

# --- PUBLIC ---
# --- PUBLIC ---
class ProjectListAPIView(generics.ListAPIView):
    """Liste publique des projets"""
    queryset = Project.objects.all().order_by('-year')
    serializer_class = ProjectSerializer
    permission_classes = []  # Public


# --- ADMIN ---
class ProjectAdminAPIView(viewsets.ModelViewSet):
    """CRUD complet pour l'admin"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAdminUser]
