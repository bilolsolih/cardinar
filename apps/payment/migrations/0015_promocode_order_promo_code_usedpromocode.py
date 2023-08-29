# Generated by Django 4.1.5 on 2023-03-17 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0028_alter_course_options_alter_coursecomment_options_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('payment', '0014_alter_installmentlog_options_alter_order_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='Code')),
                ('percent', models.PositiveSmallIntegerField(verbose_name='Percent')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course', verbose_name='Course')),
            ],
            options={
                'verbose_name': 'Promo Code',
                'verbose_name_plural': 'Promo Codes',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Promo code'),
        ),
        migrations.CreateModel(
            name='UsedPromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.order', verbose_name='Order')),
                ('promo_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='payment.promocode', verbose_name='Promo Code')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Used Promo Code',
                'verbose_name_plural': 'Used Promo Codes',
                'unique_together': {('user', 'promo_code')},
            },
        ),
    ]
