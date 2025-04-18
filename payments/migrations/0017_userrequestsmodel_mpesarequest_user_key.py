# Generated by Django 4.2.7 on 2025-04-10 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0016_storebusinesscode'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserRequestsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('key', models.CharField(max_length=255)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payments.storebusinesscode')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='mpesarequest',
            name='user_key',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.userrequestsmodel'),
        ),
    ]
