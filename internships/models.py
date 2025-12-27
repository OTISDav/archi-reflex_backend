from django.db import models

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
    cv = models.FileField(upload_to='internships/cv/')
    letter = models.FileField(upload_to='internships/letters/')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
