from rest_framework.routers import DefaultRouter
from .views import ProjectAdminAPIView, ProjectListAPIView
from django.urls import path

router = DefaultRouter()
router.register(r'projects/admin', ProjectAdminAPIView, basename='project-admin')

urlpatterns = [
    path('projects/', ProjectListAPIView.as_view()),
]

urlpatterns += router.urls
