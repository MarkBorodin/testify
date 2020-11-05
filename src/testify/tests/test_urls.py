from django.test import Client, TestCase
from django.urls import reverse


class TestUrls(TestCase):

    fixtures = [
        'tests/fixtures/dump.json'
    ]

    def setUp(self):
        self.client = Client()

    def tearDown(self):
        pass

    def test_urls_public_availability(self):
        urls = [
            reverse('core:index'),
            reverse('accounts:register'),
            reverse('accounts:login'),
        ]

        for url in urls:
            response = self.client.get(url)
            assert response.status_code == 200

    def test_urls_private_availability(self):
        urls = [
            reverse('tests:list'),
            reverse('tests:details', args=(1,)),
            reverse('tests:start', args=(1,)),
            reverse('tests:next', args=(1,)),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)
            # assert response.url == reverse('accounts:login')
            self.assertEqual(response.url.startswith(reverse('accounts:login')), True)

    def test_urls_private_authenticated_availability(self):
        urls = [
            reverse('tests:list'),
            reverse('tests:details', args=(1,)),
        ]

        self.client.login(username='superadmin', password='superadmin')

        for url in urls:
            response = self.client.get(url)
            assert response.status_code == 200

    def test_urls_public_authenticated_availability(self):
        urls = [
            reverse('core:index'),
            reverse('accounts:register'),
            reverse('accounts:login'),
        ]

        self.client.login(username='superadmin', password='superadmin')

        for url in urls:
            response = self.client.get(url)
            assert response.status_code == 200
