# Generated by Django 4.2.6 on 2023-10-16 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0007_customorder'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='type',
        ),
    ]
