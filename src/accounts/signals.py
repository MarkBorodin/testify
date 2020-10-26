from accounts.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from testify.models import TestResult


@receiver(post_save, sender=TestResult)
def update_rating(sender, instance, created, **kwargs):
    if instance.state == TestResult.STATE.FINISHED:
        user = User.objects.get(username=instance.user)
        current_rating = user.rating
        new_rating = current_rating + instance.points()
        user.rating = new_rating
        user.save()
