from django.test import Client, TestCase
from django.urls import reverse

from testify.forms import AnswerFormSet
from testify.models import Test


class TestDetailsViewTest(TestCase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]

    def setUp(self):
        self.client = Client()
        self.client.login(username='superadmin', password='superadmin')

    def test_details(self):
        response = self.client.get(reverse('tests:details', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context_data.get('test'))


class TestRunnerView(TestCase):
    fixtures = [
        'tests/fixtures/dump.json',
    ]
    TEST_ID = 1

    def setUp(self):
        self.client = Client()
        self.client.login(username='superadmin', password='superadmin')

    def test_basic_flow(self):
        response = self.client.get(reverse('tests:start', kwargs={'id': self.TEST_ID}))
        self.assertRedirects(response, reverse('tests:next', kwargs={'id': self.TEST_ID}))

        test = Test.objects.get(id=self.TEST_ID)

        for question in test.questions.order_by('order_number'):
            next_url = reverse('tests:next', args=(self.TEST_ID,))
            response = self.client.get(next_url)

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Next')

            response = self.client.post(
                path=next_url,
                data={
                    'form-TOTAL_FORMS': '4',
                    'form-INITIAL_FORMS': '4',
                    'form-MIN_NUM_FORMS': '0',
                    'form-MAX_NUM_FORMS': '1000',
                    'form-0-is_selected': 'on',
                },
            )
            if question.order_number < test.questions.count():
                self.assertRedirects(response, next_url)
            else:
                self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Congratulations!!!')

    # def test_success_flow(self):
    #     response = self.client.get(reverse('tests:start', kwargs={'id': self.TEST_ID}))
    #     self.assertRedirects(response, reverse('tests:next', kwargs={'id': self.TEST_ID}))
    #
    #     test = Test.objects.get(id=self.TEST_ID)
    #
    #     for question in test.questions.order_by('order_number'):
    #         next_url = reverse('tests:next', args=(self.TEST_ID,))
    #         response = self.client.get(next_url)
    #
    #         self.assertEqual(response.status_code, 200)
    #         self.assertContains(response, 'Next')
    #
    #         answer = question.answers.get(is_correct=True) # noqa
    #
    #         answers = question.answers.all()
    #         form_set = AnswerFormSet(queryset=answers)   # noqa
    #
    #         response = self.client.post(
    #             path=next_url,
    #             data={
    #                 'form-TOTAL_FORMS': '4',
    #                 'form-INITIAL_FORMS': '4',
    #                 'form-MIN_NUM_FORMS': '0',
    #                 'form-MAX_NUM_FORMS': '1000',
    #                 'form-0-is_selected': 'on',
    #             }
    #         )
    #         if question.order_number < test.questions.count():
    #             self.assertRedirects(response, next_url)
    #         else:
    #             self.assertEqual(response.status_code, 200)
    #
    #     self.assertContains(response, 'Congratulations!!!')
