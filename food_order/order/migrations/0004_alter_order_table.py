# Generated by Django 5.0.1 on 2024-01-28 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_remove_order_cart_order_carts'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
    ]
