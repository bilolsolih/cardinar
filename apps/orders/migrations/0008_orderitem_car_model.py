# Generated by Django 4.2.1 on 2023-09-14 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_premiumphoto'),
        ('orders', '0007_alter_orderitem_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='car_model',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='store.carmodel', verbose_name='Car model'),
            preserve_default=False,
        ),
    ]
