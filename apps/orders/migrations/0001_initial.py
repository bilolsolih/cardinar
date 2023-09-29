# Generated by Django 4.2.1 on 2023-09-28 11:11

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=128, verbose_name='Full name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='UZ', verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('delivery_type', models.CharField(choices=[('s', 'Self-picked'), ('d', 'Delivery')], max_length=1, verbose_name='Delivery type')),
                ('city', models.CharField(blank=True, max_length=128, null=True, verbose_name='Destination city')),
                ('region', models.CharField(blank=True, max_length=128, null=True, verbose_name='Region')),
                ('address', models.CharField(blank=True, max_length=128, null=True, verbose_name='Address')),
                ('level', models.CharField(blank=True, max_length=128, null=True, verbose_name='Floor number')),
                ('delivery_date', models.DateField(blank=True, null=True, verbose_name='Delivery date')),
                ('is_paid', models.BooleanField(default=False, verbose_name='Is Paid')),
                ('is_canceled', models.BooleanField(default=False, verbose_name='Is Canceled')),
                ('status', models.CharField(choices=[('d', 'Delivered'), ('p', 'Pending')], default='p', max_length=1, verbose_name='Status')),
                ('payment_status', models.CharField(choices=[('wp', 'Waiting for payment'), ('pd', 'Paid')], default='wp', max_length=2, verbose_name='Payment status')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('store', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='store.store', verbose_name='Store')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='PaymentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('title_ru', models.CharField(max_length=128, null=True, verbose_name='Title')),
                ('title_uz', models.CharField(max_length=128, null=True, verbose_name='Title')),
            ],
            options={
                'verbose_name': 'Payment type',
                'verbose_name_plural': 'Payment types',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Quantity')),
                ('cost', models.PositiveIntegerField(blank=True, null=True, verbose_name='Cost')),
                ('articul', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.articul')),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='store.carmodel', verbose_name='Car model')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.order', verbose_name='Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_items', to='store.product', verbose_name='Product')),
            ],
            options={
                'verbose_name': 'Order item',
                'verbose_name_plural': 'Order items',
            },
        ),
    ]
