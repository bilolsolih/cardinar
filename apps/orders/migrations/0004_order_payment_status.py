# Generated by Django 4.2.1 on 2023-08-28 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_paymenttype_title_en'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('wp', 'Waiting for payment'), ('pd', 'Paid')], default='wp', max_length=2, verbose_name='Payment status'),
        ),
    ]