from django.test import TestCase


class TestViews(TestCase):

    def test_superUserview(self):
        self.client.login(username='admin', password='')
        response = self.client.get('mainforms/superuser.html', follow=True)
