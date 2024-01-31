# Generated by Django 5.0.1 on 2024-01-28 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_alter_order_cart'),
        ('products', '0011_remove_cart_item_cart_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cart',
        ),
        migrations.AddField(
            model_name='order',
            name='carts',
            field=models.ManyToManyField(to='products.cart', verbose_name='Product carts'),
        ),
    ]