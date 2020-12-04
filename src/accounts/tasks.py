import datetime
import time

from celery import shared_task
from django.core.mail import send_mail

from accounts.models import User
from django.conf import settings
from testify.models import TestResult


@shared_task
def check_tests(id):
    result = TestResult.objects.filter(user=id)
    if result.count() == 0:
        user = User.objects.get(id=id)
        send_mail(
            subject="Hi! You haven't completed any test yet",
            message='Take your first test: www.testify.com',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
