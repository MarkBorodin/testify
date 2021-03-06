import datetime

from core.utils import resize_image

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(null=True, default='default.jpg', upload_to='pics/')
    interests = models.CharField(max_length=128, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    rating = models.SmallIntegerField(null=True, blank=True, default=0)
    num_emails_received = models.SmallIntegerField(null=True, blank=True, default=0)
    last_email_sent = models.DateTimeField(null=True, blank=True, default=datetime.datetime.utcfromtimestamp(0))

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        resize_image(self.image)
        return result

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
