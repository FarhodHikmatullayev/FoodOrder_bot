from django.db import models


class Order(models.Model):
    user = models.ForeignKey('users.User', models.CASCADE)
    carts = models.ManyToManyField('products.Cart', verbose_name='Product carts')
    name = models.CharField(verbose_name='Ism', max_length=221)
    phone = models.CharField(verbose_name='Telefon raqam', max_length=17)
    total_price = models.DecimalField(verbose_name="Narx", decimal_places=2, max_digits=8)

    # created_time = models.DateTimeField(auto_now_add=True)
    # updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} price={self.total_price}$"

    class Meta:
        db_table = 'order'
