# Create your models here.
import datetime

from django.conf import settings
from django.db import models


class BlacklistedToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"BlacklistedToken for {self.user} created at {self.created_at}"

    @property
    def is_expired(self):
        return datetime.datetime.now() >= self.expires_at
