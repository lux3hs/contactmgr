# Generated by Django 3.1.6 on 2021-04-07 20:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0039_auto_20210402_0253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entitlement',
            name='allowed_ips',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='creation_date',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='creator_email',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='creator_phone',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='expiration_date',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='host_ip',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='is_permanent',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='product_grade',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='product_stations',
        ),
        migrations.RemoveField(
            model_name='entitlement',
            name='re_seller',
        ),
    ]
