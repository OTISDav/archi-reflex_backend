from rest_framework import serializers
from .models import Appointment
from datetime import date as date_class

class PublicAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('status', 'google_event_id', 'created_at')

    def validate(self, data):
        date = data.get("date")
        time = data.get("time")

        # Vérifier que la date n'est pas dans le passé
        if date < date_class.today():
            raise serializers.ValidationError("La date du RDV ne peut pas être passée.")

        # Vérifier si créneau déjà pris
        qs = Appointment.objects.filter(date=date, time=time).exclude(status="rejected")
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ce créneau est déjà occupé. Merci de choisir une autre heure.")

        return data

class AdminAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('google_event_id', 'created_at')

    def validate(self, data):
        # Même validation de créneau que le public
        date = data.get("date", self.instance.date if self.instance else None)
        time = data.get("time", self.instance.time if self.instance else None)
        qs = Appointment.objects.filter(date=date, time=time).exclude(status="rejected")
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ce créneau est déjà occupé. Merci de choisir une autre heure.")
        return data
