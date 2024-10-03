from django.db import models
from django.contrib.auth.models import User

class GPSTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_lat = models.FloatField()
    start_lon = models.FloatField()
    end_lat = models.FloatField()
    end_lon = models.FloatField()
    mileage = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
