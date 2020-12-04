import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from testify.models import TestResult


@shared_task
def motivation_letter():
    results = TestResult.objects.filter(
        state=TestResult.STATE.NEW,
        write_date__lte=datetime.datetime.now() - datetime.timedelta(seconds=5*24*3600)
    )
    for result in results:
        send_mail(
            subject="Hi! You have unfinished test",
            message='Continue your test: www.testify.com',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[result.user.email],
            fail_silently=False,
        )

    print('email sent!')
