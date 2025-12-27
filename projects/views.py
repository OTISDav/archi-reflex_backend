from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
