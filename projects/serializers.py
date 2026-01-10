from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_image(self, obj):
        if obj.image:
            if isinstance(obj.image, str):
                return obj.image  # si c'est déjà une URL (upload Cloudinary)
            return obj.image.url  # sinon CloudinaryField
        return None
