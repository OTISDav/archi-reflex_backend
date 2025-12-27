from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.conf import settings
from .serializers import ContactSerializer
from .models import ContactMessage
from core.emails import send_notification

# --- PUBLIC ---
class ContactAPIView(APIView):
    """Formulaire de contact public"""
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        send_notification(
            f"Message de {serializer.validated_data['name']}",
            serializer.validated_data['message'],
            settings.ADMIN_EMAIL
        )
        return Response({"success": True})

# --- ADMIN ---
class ContactAdminAPIView(generics.ListAPIView):
    """Permet à l'admin de voir tous les messages"""
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAdminUser]

