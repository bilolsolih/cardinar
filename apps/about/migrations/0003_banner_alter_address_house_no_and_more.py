# Generated by Django 4.2.1 on 2023-07-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_rename_district_de_address_district_ru_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
                ('photo', models.ImageField(upload_to='images/about/banners/', verbose_name='Photo')),
                ('text', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('text_ru', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('text_en', models.TextField(blank=True, null=True, verbose_name='Text')),
                ('text_uz', models.TextField(blank=True, null=True, verbose_name='Text')),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
            },
        ),
        migrations.AlterField(
            model_name='address',
            name='house_no',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='House number'),
        ),
        migrations.AlterUniqueTogether(
            name='socialmedia',
            unique_together={('social_media', 'link')},
        ),
    ]
