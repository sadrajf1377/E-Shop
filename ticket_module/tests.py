from django.test import TestCase
from django.urls import reverse

from user_Module.models import normal_user
# Create your tests here.
class Test_Ticket_Views(TestCase):
    def setUp(self):
        data={'ticket_title':'title'}
        self.ticket_creation_test_not_auth = self.client.post(reverse('create_new_tickets'), data=data).status_code
        user=normal_user.objects.create_user(username='test1',email='test@test.com')
        user.set_password('1234')
        user.save()
        self.client.login(username='test1',password='1234')
        self.ticket_creation_test_auth=self.client.post(reverse('create_new_tickets'),data=data).status_code

    def test(self):
        self.assertEqual(self.ticket_creation_test_auth,201,msg='failed to create a ticket as an authenticated user')
        self.assertNotEqual(self.ticket_creation_test_not_auth, 201, msg='created a ticket as a not authenticated user')