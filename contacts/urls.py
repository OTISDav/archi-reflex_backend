from django.urls import path
from .views import ContactAPIView, ContactAdminAPIView

urlpatterns = [
    path('contact/', ContactAPIView.as_view()),
    path('admin/', ContactAdminAPIView.as_view()),
]
