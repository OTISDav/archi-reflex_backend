from django.urls import path
from .views import (
    AppointmentCreateAPIView,
    AppointmentAdminAPIView,
)

urlpatterns = [
    path("appointments/", AppointmentCreateAPIView.as_view(), name="appointment-create"),

    path("admin/appointments/", AppointmentAdminAPIView.as_view(), name="admin-appointments-list"),

    path("admin/appointments/<int:pk>/", AppointmentAdminAPIView.as_view(), name="admin-appointments-update"),
]
