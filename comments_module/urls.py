from django.urls import path
from .views import send_comment
urlpatterns=[path('send-comment',send_comment.as_view(),name='send-comment')]