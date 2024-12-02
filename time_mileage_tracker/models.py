from django.db import models
from django.contrib.auth.models import User


class RouteLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    distance = models.FloatField()
    duration = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Signup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.user.username}: {self.start_location} -> {self.end_location}"


