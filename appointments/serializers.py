from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("google_event_id", "created_at", "status")

    def validate(self, data):
        date = data.get("date") or getattr(self.instance, "date", None)
        time = data.get("time") or getattr(self.instance, "time", None)

        qs = Appointment.objects.filter(date=date, time=time).exclude(status="cancelled")
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                f"Ce créneau du {date} à {time} est déjà pris."
            )

        return data

    def validate_status(self, value):
        request = self.context.get("request")

        if request and request.method in ["PATCH", "PUT"]:
            if not request.user.is_staff:
                raise serializers.ValidationError(
                    "Vous n'êtes pas autorisé à modifier le statut."
                )

        return value
