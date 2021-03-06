from accounts.models import User

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail

from testify.models import TestResult


@shared_task
def check_tests(id): # noqa
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


@shared_task
def trial_lesson_email(subject, message, from_email, recipient_list, fail_silently):
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=fail_silently,
    )
