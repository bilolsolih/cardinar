# Generated by Django 4.2.1 on 2023-08-30 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_payment_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='order',
            name='is_canceled',
            field=models.BooleanField(default=False, verbose_name='Is Canceled'),
        ),
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Is Paid'),
        ),
    ]