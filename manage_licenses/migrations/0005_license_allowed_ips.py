# Generated by Django 3.1.6 on 2021-03-11 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_licenses', '0004_auto_20210311_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='license',
            name='allowed_ips',
            field=models.IntegerField(default=10),
        ),
    ]
