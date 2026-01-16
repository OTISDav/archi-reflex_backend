from django.urls import path
from .views import ContactAPIView, ContactAdminAPIView
from . import views

urlpatterns = [
    path('contact/', ContactAPIView.as_view()),
    path('admin/', ContactAdminAPIView.as_view()),

    path('health/', views.health_check, name='health_check'),
]
