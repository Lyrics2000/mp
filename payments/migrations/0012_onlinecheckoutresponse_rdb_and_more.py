# Generated by Django 4.2.7 on 2024-06-22 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0011_mpesarequest_callback_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlinecheckoutresponse',
            name='rdb',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.mpesarequest'),
        ),
        migrations.AlterField(
            model_name='mpesacallbackmetadata',
            name='rdb',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.mpesarequest'),
        ),
        migrations.AlterField(
            model_name='onlinecheckoutresponse',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]