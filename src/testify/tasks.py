import datetime

from accounts.models import User

from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from testify.models import TestResult


@shared_task
def motivation_letter():
    results = TestResult.objects.filter(
        state=TestResult.STATE.NEW,
        write_date__lte=datetime.datetime.now() - datetime.timedelta(seconds=5*24*3600)
    )
    for result in results:
        user = User.objects.get(id=result.user.id)
        timedelta = user.last_email_sent + datetime.timedelta(days=90)
        if user.num_emails_received < 2 and timezone.now() > timedelta:
            user.num_emails_received += 1
            user.last_email_sent = datetime.datetime.now()
            user.save()
            send_mail(
                subject="Hi! You have unfinished test",
                message='Continue your test: www.testify.com',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[result.user.email],
                fail_silently=False,
            )

    print('email sent!')
