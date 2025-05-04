from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    description = models.TextField()
    features = models.TextField(help_text="List of features (e.g., projector, whiteboard)")
    status = models.CharField(
        max_length=20,
        choices=[
            ('available', 'Available'),
            ('maintenance', 'Under Maintenance'),
        ],
        default='available'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
