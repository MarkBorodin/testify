from django.test import TestCase, override_settings


@override_settings(
    CELERY_TASK_ALWAYS_EAGER=True,
    CELERY_TASK_EAGER_PROPOGATES=True,
)
class TestCaseBase(TestCase):
    pass
