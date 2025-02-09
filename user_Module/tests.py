from django.test import TestCase
from django.urls import reverse
from user_Module.models import normal_user


class TestEditUserInfoView(TestCase):
    def setUp(self):
        self.user = normal_user.objects.create_user(username='username',email='email@email.com')
        self.user.set_password('1234')
        self.user.save()
        print('my user is',self.user)
        self.client.login(username='username', password='1234')

        self.url = reverse('edit_user_info')
        self.response = self.client.get(self.url)

    def test_edit_user_info_view(self):
        self.assertEqual(self.response.status_code, 200, msg='Failed to load edit user info view.')

        self.assertTemplateUsed(self.response, 'edit_user_information.html')

        self.assertContains(self.response, "Edit Your Information", msg_prefix='The page content is not as expected.')
