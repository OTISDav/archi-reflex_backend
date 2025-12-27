from django.urls import path
from .views import InternshipCreateAPIView, InternshipAdminAPIView

urlpatterns = [
    path('internships/', InternshipCreateAPIView.as_view()),
    path('admin/', InternshipAdminAPIView.as_view()),
    path('admin/<int:pk>/', InternshipAdminAPIView.as_view()),
]
