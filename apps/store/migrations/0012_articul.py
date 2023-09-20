# Generated by Django 4.2.1 on 2023-09-20 12:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_product_is_constructable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Articul',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='articuls', to='store.carmodel')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articuls', to='store.product')),
            ],
            options={
                'verbose_name': 'Articul',
                'verbose_name_plural': 'Articuls',
            },
        ),
    ]
