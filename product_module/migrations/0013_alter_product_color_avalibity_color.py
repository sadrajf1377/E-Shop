# Generated by Django 4.2 on 2024-03-04 19:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0012_alter_product_wish_list_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_color_avalibity',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.colors', verbose_name='product color'),
        ),
    ]
