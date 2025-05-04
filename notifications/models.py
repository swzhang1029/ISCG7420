from django.db import models
from django.contrib.auth.models import User
from bookings.models import Booking

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    notification_type = models.CharField(
        max_length=20,
        choices=[
            ('confirmation', 'Booking Confirmation'),
            ('cancellation', 'Booking Cancellation'),
            ('reminder', 'Booking Reminder'),
        ]
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.notification_type}"

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]
