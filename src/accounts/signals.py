import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from accounts.tasks import check_tests
from testify.models import TestResult


@receiver(post_save, sender=TestResult)
def update_rating(sender, instance, created, **kwargs):
    if instance.state == TestResult.STATE.FINISHED:
        user = instance.user
        current_rating = user.rating
        new_rating = current_rating + instance.points()
        user.rating = new_rating
        user.save()


@receiver(post_save, sender=User)
def email_new_user(sender, instance, created, **kwargs):
    if created:
        check_tests.apply_async(args=(instance.id,), eta=datetime.datetime.now() + datetime.timedelta(minutes=5))
