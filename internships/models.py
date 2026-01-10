from django.db import models
from cloudinary.models import CloudinaryField

class Internship(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Accepté'),
        ('rejected', 'Refusé'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    school = models.CharField(max_length=100)
    message = models.TextField()
    cv = CloudinaryField('cv', resource_type='raw')
    letter = CloudinaryField('letter', resource_type='raw')  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.school}"
