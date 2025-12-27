from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from core.emails import send_notification
from .serializers import InternshipSerializer

class InternshipCreateAPIView(APIView):
    def post(self, request):
        serializer = InternshipSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        internship = serializer.save()

        send_notification(
            "Demande de stage reçue",
            "Votre candidature a bien été reçue.",
            internship.email
        )

        send_notification(
            "Nouvelle demande de stage",
            f"Candidat : {internship.name}",
            settings.ADMIN_EMAIL
        )

        return Response(serializer.data, status=201)
