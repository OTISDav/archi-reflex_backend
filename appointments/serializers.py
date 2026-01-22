from rest_framework import serializers
from .models import Appointment
from datetime import date as date_class

# ==========================
# Serializer pour le client
# ==========================
class PublicAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            "name", "email", "phone",
            "project_type", "message",
            "date", "time"
        )

    def validate(self, data):
        date = data.get("date")
        time = data.get("time")

        # ✅ La date ne peut pas être dans le passé
        if date < date_class.today():
            raise serializers.ValidationError("La date du RDV ne peut pas être passée.")

        # ✅ Vérifier si le créneau est déjà occupé (sauf refusés)
        if Appointment.objects.filter(date=date, time=time).exclude(status="rejected").exists():
            raise serializers.ValidationError("Ce créneau est déjà occupé.")

        return data


# ==========================
# Serializer pour l'admin
# ==========================
class AdminAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "project_type",
            "message",
            "date",
            "time",
            "status",
            "created_at",
        )
        # fields = ("id", "status")  # id inclus pour React

    def validate_status(self, value):
        # ✅ Statut valide uniquement
        if value not in ["accepted", "rejected"]:
            raise serializers.ValidationError("Statut invalide.")

        # 🔒 Empêcher rejected → accepted côté backend
        if self.instance and self.instance.status == "rejected" and value == "accepted":
            raise serializers.ValidationError("Impossible de confirmer un RDV déjà refusé.")

        return value
