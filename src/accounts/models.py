from core.utils import resize_image

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(null=True, default='default.jpg', upload_to='pics/')
    interests = models.CharField(max_length=128, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    rating = models.SmallIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        resize_image(self.image)
        return result
