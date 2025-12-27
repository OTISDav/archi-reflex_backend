from django.urls import path
from .views import AppointmentCreateAPIView

urlpatterns = [
    path('appointments/', AppointmentCreateAPIView.as_view()),
]
