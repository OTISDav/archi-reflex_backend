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
            url = obj.cv.url if hasattr(obj.cv, 'url') else obj.cv
            # Forcer l'extension PDF si absente
            if not url.lower().endswith(('.pdf', '.doc', '.docx')):
                url += '.pdf'
            return url
        return None

    def get_letter(self, obj):
        if obj.letter:
            url = obj.letter.url if hasattr(obj.letter, 'url') else obj.letter
            if not url.lower().endswith(('.pdf', '.doc', '.docx')):
                url += '.pdf'
            return url
        return None

    def validate_cv(self, file):
        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("Le CV doit être en PDF.")
        return file

    def validate_letter(self, file):
        if not file.name.lower().endswith('.pdf'):
            raise serializers.ValidationError("La lettre doit être en PDF.")
        return file
