# Generated by Django 4.2 on 2024-01-25 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0006_products_has_color_instances'),
    ]

    operations = [
        migrations.AddField(
            model_name='colors',
            name='assigned_to_all_products',
            field=models.BooleanField(default=False, verbose_name='به همه کالا ها نسبت داده شده'),
        ),
    ]
