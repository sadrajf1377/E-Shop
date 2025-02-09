from django.urls import path
from .views import show_tickets,show_ticket_details,create_new_ticket_message,new_ticket,show_user_tickects,answer_ticket
urlpatterns=[
    path('my_tickets',show_user_tickects.as_view(),name='my_tickets'),
    path('ticket_details/<title>',show_ticket_details.as_view(),name='ticket_details'),
    path('create_new_ticket',new_ticket.as_view(),name='create_new_ticket'),
    path('show_users_tickets_admin',show_tickets.as_view(),name='show_user_tickets'),
    path('create_ticket_message',create_new_ticket_message.as_view(),name='new_ticket_message'),
    path('answer_ticket',answer_ticket.as_view(),name='answer_ticket'),


]