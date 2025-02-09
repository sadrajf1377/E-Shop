from django.test import TestCase
from django.urls import reverse
from .models import products
from comments_module.models import comment
from user_Module.models import normal_user
# Create your tests here.
class Test_Views(TestCase):
    def setUp(self):
        self.index_view=self.client.get(reverse('load_index_Page')).status_code
        self.invalid_product_details_view=self.client.get(reverse('show-product-details',args=['-1'])).status_code
        self.product=products(title='product',url='test')
        self.product.save()
        self.user=normal_user(username='admin',email='email@email.com')
        self.user.set_password('1234')
        self.user.save()
        self.client.login(username=self.user.username,password='1234')
        self.comment=comment(comment_text='text',product=self.product,user=self.user)
        self.comment.save()
        self.product_details_view=self.client.get(reverse('show-product-details',args=['test']))




    def test_views(self):
        self.assertEqual(self.index_view,200,msg='index page view ran successfully')
        self.assertEqual(self.invalid_product_details_view,404, msg='product details view didnt retrun 404 status code when an invalid id was given to it')
        self.assertIn(self.comment,self.product.comment_set.all(),msg='the parent post of comment was not set properly')



