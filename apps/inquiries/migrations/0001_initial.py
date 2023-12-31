# Generated by Django 4.2.1 on 2023-10-03 12:07

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
            name='Inquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('full_name', models.CharField(max_length=128, verbose_name='Full name')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone number')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Comment')),
                ('is_one_click', models.BooleanField(default=False)),
                ('is_call', models.BooleanField(default=False)),
                ('is_product', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True, verbose_name='Active?')),
                ('articul', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inquiries', to='store.articul')),
                ('on_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inquiries', to='store.product', verbose_name='On product')),
            ],
            options={
                'verbose_name': 'Inquiry on product',
                'verbose_name_plural': 'Inquiries on product',
            },
        ),
        migrations.CreateModel(
            name='InquiryCall',
            fields=[
            ],
            options={
                'verbose_name': 'Inquiry for call',
                'verbose_name_plural': 'Inquiries for call',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('inquiries.inquiry',),
        ),
        migrations.CreateModel(
            name='InquiryOneClick',
            fields=[
            ],
            options={
                'verbose_name': 'Inquiry for One-click-buy',
                'verbose_name_plural': 'Inquiries for One-click-buy',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('inquiries.inquiry',),
        ),
    ]
