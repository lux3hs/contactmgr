# Generated by Django 4.1.1 on 2022-10-16 03:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_contacts', '0047_rename_organization_product_product_org'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='page_tab',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='phone',
        ),
    ]
