# Generated by Django 4.2 on 2025-01-26 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=20, null=True, verbose_name='عنوان نظر')),
                ('comment_text', models.TextField(blank=True, max_length=100, null=True, verbose_name='متن نظر')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments_module.comment', verbose_name='والد')),
            ],
        ),
    ]
