# Generated by Django 4.2 on 2024-01-25 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0005_alter_products_brand_alter_products_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='has_color_instances',
            field=models.BooleanField(default=False, verbose_name='وجود رنگ های مختلف ازاین محصول'),
        ),
    ]
