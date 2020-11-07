from django.test import TestCase

from testify.models import Test


class TestResultModelTests(TestCase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.test = Test.objects.first()

    def test_points(self):
        for test_result in self.test.test_results.all():
            self.assertEqual(test_result.points() < Test.QUESTION_MAX_LIMIT, True)

    def test_score(self):
        for test_result in self.test.test_results.all():
            self.assertEqual(test_result.score() <= 100, True)
