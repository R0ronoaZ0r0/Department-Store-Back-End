# Generated by Django 4.2 on 2023-04-30 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_order_order_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='zip',
        ),
    ]