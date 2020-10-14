from PIL import Image

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class IMAGE_SIZE(models.IntegerChoices):
        FIXED_SIZE = 300
    image = models.ImageField(null=True, default='default.jpg', upload_to='pics/')
    interests = models.CharField(max_length=128, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    @staticmethod
    def resize_image(image, size=(300, 300)):
        original_image = Image.open(image)
        width, height = original_image.size

        if width > User.IMAGE_SIZE.FIXED_SIZE or height > User.IMAGE_SIZE.FIXED_SIZE:
            if width == height:
                resized_image = original_image.resize(size)
                return resized_image.save(image.file.name)
            else:
                if width > height:
                    new_width = User.IMAGE_SIZE.FIXED_SIZE
                    new_height = int(new_width * height / width)
                else:
                    new_height = User.IMAGE_SIZE.FIXED_SIZE
                    new_width = int(new_height * width / height)
                resized_image = original_image.resize((new_width, new_height), Image.ANTIALIAS)
                return resized_image.save(image.file.name)

    def save(self):
        result = super().save()
        self.resize_image(self.image)
        return result
