# Generated by Django 4.2.1 on 2023-09-28 05:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_liked_products'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertoken',
            options={'ordering': ['created'], 'verbose_name': 'User token', 'verbose_name_plural': 'User tokens'},
        ),
        migrations.AddField(
            model_name='usertoken',
            name='is_expired',
            field=models.BooleanField(default=False, verbose_name='Is expired?'),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]