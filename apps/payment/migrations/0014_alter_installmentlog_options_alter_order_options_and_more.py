# Generated by Django 4.1.5 on 2023-03-14 15:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0013_alter_installmentlog_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='installmentlog',
            options={'verbose_name': 'Installment Log', 'verbose_name_plural': 'Installment Logs'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='paymentmerchantrequestlog',
            options={'verbose_name': 'Payment Merchant Request Log', 'verbose_name_plural': 'Payment Merchant Request Logs'},
        ),
        migrations.AlterModelOptions(
            name='transaction',
            options={'verbose_name': 'Transaction', 'verbose_name_plural': 'Transactions'},
        ),
    ]