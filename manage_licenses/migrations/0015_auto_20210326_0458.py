# Generated by Django 3.1.6 on 2021-03-26 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_licenses', '0014_auto_20210315_2240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='license',
            old_name='IP_Host',
            new_name='host_ip',
        ),
    ]
