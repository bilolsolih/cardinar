# Generated by Django 4.1.5 on 2023-02-15 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0008_usercard_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercard',
            name='confirmed',
            field=models.BooleanField(default=False, verbose_name='Confirmed'),
        ),
    ]