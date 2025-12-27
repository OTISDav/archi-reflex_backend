from django.urls import path
from .views import AppointmentCreateAPIView, AppointmentAdminAPIView

urlpatterns = [
    path('appointments/', AppointmentCreateAPIView.as_view()),
    path('admin/', AppointmentAdminAPIView.as_view()),
    path('admin/<int:pk>/', AppointmentAdminAPIView.as_view()),
]
