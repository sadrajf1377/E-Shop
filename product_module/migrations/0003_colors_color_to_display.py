# Generated by Django 4.2 on 2023-12-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0002_product_color_avalibity'),
    ]

    operations = [
        migrations.AddField(
            model_name='colors',
            name='color_to_display',
            field=models.CharField(default='white', max_length=30, verbose_name='رنگ html'),
        ),
    ]
