# Generated by Django 3.2.9 on 2021-12-04 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_shoppinglist_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shoppingitem',
            old_name='last_update',
            new_name='last_update_date',
        ),
        migrations.RenameField(
            model_name='shoppinglist',
            old_name='last_update',
            new_name='last_update_date',
        ),
    ]
