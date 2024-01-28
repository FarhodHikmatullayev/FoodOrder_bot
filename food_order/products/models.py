from django.db import models


# from food_order.users.models import User


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    productname = models.CharField(verbose_name="Mahsulot nomi", max_length=50)
    photo = models.CharField(verbose_name="Rasm file_id", max_length=200, null=True)
    price = models.DecimalField(verbose_name="Narx", decimal_places=2, max_digits=8)
    description = models.TextField(verbose_name="Mahsulot haqida", max_length=3000, null=True)

    category_code = models.CharField(verbose_name="Kategoriya kodi", max_length=20)
    category_name = models.CharField(verbose_name="Kategoriya nomi", max_length=30)
    subcategory_code = models.CharField(verbose_name="Ost-kategoriya kodi", max_length=20)
    subcategory_name = models.CharField(verbose_name="Ost-kategoriya nomi", max_length=30)

    def __str__(self):
        return f"№{self.id} - {self.productname}"

    class Meta:
        db_table = 'products'


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.user.full_name}'s cart"

    class Meta:
        db_table = 'cart'
