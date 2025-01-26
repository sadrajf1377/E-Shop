from django.contrib.auth.models import AbstractUser
from django.urls import path

from user_Module import models
from .views import edit_user_info,ask_for_password_reset,change_password,my_favourites,my_debts
from .views import change_preferred_language

urlpatterns=[path('edit_user_info/',edit_user_info.as_view(),name='edit_user_info')
             ,path('ask_for_password_reset',ask_for_password_reset.as_view(),name='ask_for_password_reset')
             ,path('reset_password/<reset_code>',change_password,name='reset_password')

             ,path('user_favourite_products/',my_favourites.as_view(),name='my_favourite_products')
            ,path('user_debts/',my_debts.as_view(),name='my_debts')
            
,path('change_language/<language>', change_preferred_language, name='change_language')

             ]