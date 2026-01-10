from django.db import models
from cloudinary.models import CloudinaryField

class Project(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    project_type = models.CharField(max_length=100)
    year = models.IntegerField()
    image = CloudinaryField('image', resource_type='image')  # <-- Cloudinary
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
