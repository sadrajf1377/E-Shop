# Generated by Django 4.2 on 2024-01-28 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0009_alter_product_article_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article_picture',
            options={'verbose_name': 'تصویر مقاله', 'verbose_name_plural': 'تصاویر مقالات'},
        ),
        migrations.AlterModelOptions(
            name='product_article',
            options={'verbose_name': 'مقاله کالا', 'verbose_name_plural': 'مقالات کالا ها'},
        ),
    ]
