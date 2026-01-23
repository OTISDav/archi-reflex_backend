from rest_framework import serializers
from .models import Internship

class InternshipSerializer(serializers.ModelSerializer):
    cv = serializers.SerializerMethodField()
    letter = serializers.SerializerMethodField()

    class Meta:
        model = Internship
        fields = '__all__'
        read_only_fields = ('status', 'created_at')

    def get_cv(self, obj):
        if obj.cv:
            if isinstance(obj.cv, str):
                return obj.cv
            return obj.cv.url
        return None

    def get_letter(self, obj):
        if obj.letter:
            if isinstance(obj.letter, str):
                return obj.letter
            return obj.letter.url
        return None

    def validate_cv(self, file):
        if not file.name.endswith('.pdf'):
            raise serializers.ValidationError("Le CV doit être en PDF.")
        return file

    def validate_letter(self, file):
        if not file.name.endswith('.pdf'):
            raise serializers.ValidationError("La lettre doit être en PDF.")
        return file
