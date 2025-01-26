from django.contrib import admin
from .models import normal_user,user_false_password_attemp
from ticket_module.models import ticket_message,user_ticket
from notification_module.models import user_notifications
# Register your models here.
admin.site.register(normal_user)



class user_messages_settings(admin.ModelAdmin):
    readonly_fields = ['creation_date']

admin.site.register(user_false_password_attemp)
admin.site.register(user_notifications)
admin.site.register(user_ticket)
admin.site.register(ticket_message)