from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from core.emails import send_notification
from .serializers import ContactSerializer

class ContactAPIView(APIView):
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        send_notification(
            f"Message de {serializer.validated_data['name']}",
            serializer.validated_data['message'],
            settings.ADMIN_EMAIL
        )

        return Response({"success": True})
