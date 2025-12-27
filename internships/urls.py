from django.urls import path
from .views import InternshipCreateAPIView

urlpatterns = [
    path('internships/', InternshipCreateAPIView.as_view()),
]
