# Generated by Django 3.2.9 on 2021-12-04 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_shoppinglist_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shoppingitem',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='shoppinglist',
            options={'ordering': ['id']},
        ),
    ]
