# Generated by Django 4.2.6 on 2023-10-17 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0010_alter_wishlistitems_product_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WishListItems',
            new_name='WishListItem',
        ),
    ]
