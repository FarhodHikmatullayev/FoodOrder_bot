# Generated by Django 5.0.1 on 2024-01-26 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_cart_buyer_id_cart_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='capacity',
            field=models.IntegerField(default=1),
        ),
    ]
