# Generated by Django 4.2.6 on 2023-10-18 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0011_rename_wishlistitems_wishlistitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='customer',
        ),
    ]
