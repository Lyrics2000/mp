# Generated by Django 4.2.7 on 2023-11-24 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_alter_onlinecheckout_checkout_request_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayBillNumbers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paybill', models.CharField(max_length=255)),
                ('client_ref', models.TextField()),
                ('client_secret', models.TextField()),
                ('developmet', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
