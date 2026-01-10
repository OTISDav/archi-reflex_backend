from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()  # Retourne l'URL Cloudinary

    class Meta:
        model = Project
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            # Si c'est déjà une string (upload via perform_create), on renvoie tel quel
            if isinstance(obj.image, str):
                return obj.image
            # Sinon, on retourne l'URL CloudinaryField
            return obj.image.url
        return None

