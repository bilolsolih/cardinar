# Generated by Django 4.2.1 on 2023-08-11 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(blank=True, max_length=64, null=True, verbose_name='Device id')),
                ('object_id', models.PositiveIntegerField(verbose_name='Object id')),
                ('quantity', models.PositiveIntegerField(default=0, verbose_name='Quantity')),
                ('cost', models.DecimalField(decimal_places=2, default=0, max_digits=24, verbose_name='Cost')),
            ],
            options={
                'verbose_name': 'Cart item',
                'verbose_name_plural': 'Cart items',
            },
        ),
    ]