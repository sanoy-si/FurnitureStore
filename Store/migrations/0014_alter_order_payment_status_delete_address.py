# Generated by Django 4.2.6 on 2023-10-30 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0013_alter_wishlistitem_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('B', 'Pending'), ('A', 'Complete'), ('C', 'Failed')], default='B', max_length=1),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
