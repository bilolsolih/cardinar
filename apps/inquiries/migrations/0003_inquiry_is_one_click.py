# Generated by Django 4.2.1 on 2023-09-22 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0002_inquiry_articul'),
    ]

    operations = [
        migrations.AddField(
            model_name='inquiry',
            name='is_one_click',
            field=models.BooleanField(default=False),
        ),
    ]