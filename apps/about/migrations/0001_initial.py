# Generated by Django 4.2.1 on 2023-10-03 12:07

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=128, verbose_name='Region')),
                ('region_ru', models.CharField(max_length=128, null=True, verbose_name='Region')),
                ('region_uz', models.CharField(max_length=128, null=True, verbose_name='Region')),
                ('district', models.CharField(max_length=128, verbose_name='District')),
                ('district_ru', models.CharField(max_length=128, null=True, verbose_name='District')),
                ('district_uz', models.CharField(max_length=128, null=True, verbose_name='District')),
                ('street', models.CharField(max_length=128, verbose_name='Street')),
                ('street_ru', models.CharField(max_length=128, null=True, verbose_name='Street')),
                ('street_uz', models.CharField(max_length=128, null=True, verbose_name='Street')),
                ('house_no', models.PositiveIntegerField(blank=True, null=True, verbose_name='House number')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('photo', models.ImageField(upload_to='images/about/banners/', verbose_name='Photo')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('text_ru', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('text_uz', models.TextField(blank=True, null=True, verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emails',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True, verbose_name='Phone number')),
            ],
            options={
                'verbose_name': 'Phone number',
                'verbose_name_plural': 'Phone numbers',
            },
        ),
        migrations.CreateModel(
            name='SocialMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('social_media', models.CharField(max_length=128, verbose_name='Social Media')),
                ('link', models.URLField(verbose_name='Link')),
            ],
            options={
                'verbose_name': 'Social Media',
                'verbose_name_plural': 'Social Medias',
                'unique_together': {('social_media', 'link')},
            },
        ),
    ]
