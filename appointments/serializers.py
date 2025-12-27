from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('status', 'google_event_id', 'created_at')

    def validate(self, data):
        date = data.get("date")
        time = data.get("time")

        # RDV déjà pris (sauf rejeté)
        qs = Appointment.objects.filter(
            date=date,
            time=time
        ).exclude(status="rejected")

        # Cas mise à jour (admin)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Ce créneau est déjà occupé. Merci de choisir une autre heure."
            )

        return data
