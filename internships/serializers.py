from rest_framework import serializers
from .models import Internship

class InternshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internship
        fields = '__all__'
        read_only_fields = ('status', 'created_at')

    def validate_cv(self, file):
        if not file.name.endswith('.pdf'):
            raise serializers.ValidationError("Le CV doit être en PDF.")
        return file

    def validate_letter(self, file):
        if not file.name.endswith('.pdf'):
            raise serializers.ValidationError("La lettre doit être en PDF.")
        return file
