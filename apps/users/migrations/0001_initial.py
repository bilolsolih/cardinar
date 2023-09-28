# Generated by Django 4.2.1 on 2023-09-28 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=128, unique=True, verbose_name='Username')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='UZ', unique=True, verbose_name='Phone number')),
                ('first_name', models.CharField(max_length=128, verbose_name='First name')),
                ('last_name', models.CharField(max_length=128, verbose_name='Last name')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('liked_products', models.ManyToManyField(blank=True, related_name='liked_users', to='store.product')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128, verbose_name='Full name')),
                ('chat_id', models.CharField(max_length=64, verbose_name='Chat id')),
                ('active', models.BooleanField(default=True, verbose_name='Can receive?')),
            ],
            options={
                'verbose_name': 'Telegram user',
                'verbose_name_plural': 'Telegram users',
            },
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('token', models.CharField(max_length=128, verbose_name='Token')),
                ('is_expired', models.BooleanField(default=False, verbose_name='Is expired?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User token',
                'verbose_name_plural': 'User tokens',
                'ordering': ['created'],
            },
        ),
    ]
