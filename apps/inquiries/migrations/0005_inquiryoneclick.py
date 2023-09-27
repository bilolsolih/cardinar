# Generated by Django 4.2.1 on 2023-09-27 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inquiries', '0004_inquirycall_alter_inquiry_options_inquiry_is_call_and_more'),
    ]

    operations = [
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
