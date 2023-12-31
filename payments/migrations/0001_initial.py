# Generated by Django 4.2.7 on 2023-11-23 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MpesaRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('phoneNumber', models.CharField(max_length=255)),
                ('accountReference', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('description', models.TextField()),
                ('MerchantRequestID', models.TextField()),
                ('CheckoutRequestID', models.TextField()),
                ('ResponseCode', models.TextField()),
                ('ResponseDescription', models.TextField()),
                ('CustomerMessage', models.TextField()),
                ('callback_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MpesaCallbackMetaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('rdb', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.mpesarequest')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
