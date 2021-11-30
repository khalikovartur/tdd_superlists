from django.test import TestCase

class HomePageTest(TestCase):

    def test_home_page_returns_correct_url(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')