# Generated by Django 4.2.6 on 2023-11-08 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0015_remove_customer_phone_customer_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customorder',
            name='left_side_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='customorder',
            name='rear_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='customorder',
            name='right_side_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
