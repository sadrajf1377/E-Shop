# Generated by Django 4.2 on 2025-02-09 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='debts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0, verbose_name='amount of money you owe this use')),
                ('paid_status', models.BooleanField(default=False, verbose_name='is the amount paid')),
                ('pay_date', models.DateField(blank=True, null=True)),
                ('pay_check_proof', models.ImageField(blank=True, null=True, upload_to='recids', verbose_name='a photo of pay recid')),
            ],
        ),
    ]
