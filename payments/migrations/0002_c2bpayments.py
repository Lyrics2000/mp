# Generated by Django 4.2.7 on 2023-11-23 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='C2BPayments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TransactionType', models.CharField(blank=True, max_length=50, null=True)),
                ('TransID', models.CharField(blank=True, max_length=30, null=True)),
                ('TransTime', models.CharField(blank=True, max_length=50, null=True)),
                ('TransAmount', models.CharField(blank=True, max_length=120, null=True)),
                ('BusinessShortCode', models.CharField(blank=True, max_length=50, null=True)),
                ('BillRefNumber', models.CharField(blank=True, max_length=120, null=True)),
                ('InvoiceNumber', models.CharField(blank=True, max_length=120, null=True)),
                ('OrgAccountBalance', models.CharField(blank=True, max_length=120, null=True)),
                ('ThirdPartyTransID', models.CharField(blank=True, max_length=120, null=True)),
                ('MSISDN', models.CharField(blank=True, max_length=25, null=True)),
                ('FirstName', models.CharField(blank=True, max_length=50, null=True)),
                ('MiddleName', models.CharField(blank=True, max_length=50, null=True)),
                ('LastName', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]
