# Generated by Django 4.2 on 2025-02-09 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ticket_message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=400, verbose_name=' متن پیام')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد پیام')),
                ('is_answered', models.BooleanField(default=False, verbose_name='آیا این پیام پاسخ دارد')),
            ],
        ),
        migrations.CreateModel(
            name='user_ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='عنوان تیکت')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد تیکت')),
            ],
        ),
    ]
