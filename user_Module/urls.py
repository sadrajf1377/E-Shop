from django.contrib.auth.models import AbstractUser
from django.urls import path

from user_Module import models
from .views import edit_user_info,ask_for_password_reset,change_password,my_favourites,my_debts,show_user_notficitations,show_user_tickects,ticket_details
from .views import new_ticket,create_new_ticket_message,mark_notif_as_read

urlpatterns=[path('edit_user_info/',edit_user_info.as_view(),name='edit_user_info')
             ,path('ask_for_password_reset',ask_for_password_reset.as_view(),name='ask_for_password_reset')
             ,path('reset_password/<reset_code>',change_password,name='reset_password')
             ,path('show_user_notficitations',show_user_notficitations.as_view(),name='show_user_notficitations')
             ,path('user_favourite_products/',my_favourites.as_view(),name='my_favourite_products')
            ,path('user_debts/',my_debts.as_view(),name='my_debts')
             ,path('user_tickets/',show_user_tickects.as_view(),name='my_tickets')
             ,path('ticket_details/<title>',ticket_details.as_view(),name='ticket_dtails')
,path('new_tickets/',new_ticket.as_view(),name='new_tickets')
,path('new_ticket_message/',create_new_ticket_message.as_view(),name='new_ticket_message')
,path('mark_notif_as_read/',mark_notif_as_read.as_view(),name='mark_notif_as_read')
             ]