from django.test import TestCase
from django.urls import reverse

from .models import normal_user

class Test(TestCase):
    def setUp(self):
        user=normal_user(username='username')
        user.set_password('1234')
        user.save()
        self.client.login(username='username',password='1234')
        self.edit_user_info_view=self.client.get(reverse('edit_user_info'))

    def test(self):
        self.assertEqual(self.edit_user_info_view.status_code,200,msg='failed to run the edit user view correctly')
        self.assertTemplateUsed(self.edit_user_info_view,'edit_user_information.html')