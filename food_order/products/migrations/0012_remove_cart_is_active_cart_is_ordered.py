# Generated by Django 5.0.1 on 2024-01-28 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_remove_cart_item_cart_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='is_active',
        ),
        migrations.AddField(
            model_name='cart',
            name='is_ordered',
            field=models.BooleanField(default=False),
        ),
    ]
