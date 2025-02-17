# Generated by Django 4.2 on 2024-02-14 12:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_Module', '0002_normal_user_user_status_user_false_password_attemp'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_notifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notif_message', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(20)], verbose_name='پیام اعلان')),
                ('notif_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ اعلان')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='گیرنده اعلان')),
            ],
        ),
        migrations.DeleteModel(
            name='user_messages',
        ),
    ]
