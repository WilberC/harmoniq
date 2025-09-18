from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TidalToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tidal_token")
    access_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() >= self.expires_at
