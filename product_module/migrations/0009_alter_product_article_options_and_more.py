# Generated by Django 4.2 on 2024-01-28 07:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0008_product_article'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product_article',
            options={'verbose_name': 'قاله کالا', 'verbose_name_plural': 'مقالات کالا ها'},
        ),
        migrations.AlterField(
            model_name='product_article',
            name='product',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.products', verbose_name='محصول مقاله'),
        ),
        migrations.AlterField(
            model_name='product_article',
            name='text',
            field=models.TextField(default='', max_length=2000, verbose_name='متن مقاله'),
        ),
        migrations.CreateModel(
            name='article_picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='article_images', verbose_name='تصویر مقاله')),
                ('parent_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.products', verbose_name='محصول والد')),
            ],
        ),
    ]
