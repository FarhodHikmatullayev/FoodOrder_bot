# Generated by Django 5.0.1 on 2024-01-26 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_cart_capacity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='capacity',
            new_name='count_item',
        ),
    ]
