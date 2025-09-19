from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class TidalToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="tidal_token")
    access_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512)
    expires_at = models.DateTimeField()
    tidal_user_id = models.CharField(max_length=128, null=True, blank=True)
    tidal_email = models.EmailField(null=True, blank=True)
    tidal_username = models.EmailField(null=True, blank=True)
    tidal_country = models.CharField(max_length=20, null=True, blank=True)

    def is_expired(self):
        return timezone.now() >= self.expires_at


class Playlist(models.Model):
    class SyncStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"

    tidal_id = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=256)
    sync_status = models.CharField(
        choices=SyncStatus.choices, max_length=50, default=SyncStatus.PENDING
    )
    synced_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    tidal_id = models.CharField(max_length=128, unique=True)
    title = models.CharField(max_length=256)
    ISRC = models.CharField(max_length=50, null=True, blank=True)
    playlists = models.ManyToManyField(Playlist, related_name="songs")

    def __str__(self):
        return f"{self.title} by {self.artist}"
