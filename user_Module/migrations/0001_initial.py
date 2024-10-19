# Generated by Django 4.2 on 2023-12-22 00:17

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='normal_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('activation_code', models.CharField(blank=True, max_length=100, null=True, verbose_name='کد فعال سازی')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='شماره موبایل')),
                ('email', models.EmailField(blank=True, max_length=20, null=True, verbose_name='ایمیل')),
                ('address', models.TextField(blank=True, max_length=300, null=True, verbose_name='آدرس محل سکونت')),
                ('first_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=300, null=True, verbose_name='نام خانوادگی')),
                ('city', models.CharField(blank=True, choices=[('mashhad', 'مشهد'), ('tehran', 'تهران'), ('shiraz', 'شیراز'), ('isfahan', 'اصهان'), ('rasht', 'رشت'), ('sarry', 'ساری'), ('az', 'یزد'), ('mashhad', 'کرمان')], max_length=20, null=True, verbose_name='شهر')),
                ('postal_code', models.IntegerField(default=0, verbose_name='کد پستی')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='profiles', verbose_name='تصویر پروفایل')),
                ('reset_password_code', models.CharField(default='', max_length=100, verbose_name='کد تغییر رمز عبور')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربرها',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='user_messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(blank=True, max_length=300, null=True, verbose_name='متن پیام')),
                ('creation_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='زمان ایجاد پیام')),
                ('ssen_by_user', models.BooleanField(default=False, verbose_name='خوانده شده')),
                ('reciever_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر دریافت کننده پیام')),
            ],
            options={
                'verbose_name': 'پیام به کاربرها',
                'verbose_name_plural': 'پیام ها به کاربرها',
            },
        ),
    ]
