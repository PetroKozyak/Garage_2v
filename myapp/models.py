from datetime import date

from django.db import models
from django.contrib.auth.models import User

User._meta.get_field("email")._unique = True


class UserProfile(models.Model):
    class Meta:
        db_table = "user_profile"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    @property
    def get_cart(self):
        cart, _ = Cart.objects.get_or_create(user=self.user, data_create=date.today())
        return cart

    def __str__(self):
        return "{}".format(self.user.username)


class Category(models.Model):
    class Meta:
        db_table = "category"
        verbose_name_plural = "Categories"

    name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.name


class Dish(models.Model):
    class Meta:
        db_table = "dishes"

    category = models.ForeignKey("Category", on_delete=models.CASCADE, null=False, blank=False,
                                 related_name="items")
    name = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=50)
    price = models.IntegerField(null=False)

    def __str__(self):
        return self.name


class Cart(models.Model):
    class Meta:
        db_table = "carts"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    data_create = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    @property
    def total_price(self):
        return sum([i.total_price for i in self.items.all()])

    def __str__(self):
        return "{} Cart".format(self.user.username)


class CartItem(models.Model):
    class Meta:
        db_table = "cart_items"

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    count_items = models.IntegerField(default=1)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    @property
    def total_price(self):
        return self.count_items * self.dish.price

    def __str__(self):
        return "{}".format(self.dish)


class Order(models.Model):
    class Meta:
        db_table = "orders"

    ORDERED = 1
    PROCESSING = 2

    status_choice = ((ORDERED, "Підтверджено"),
                     (PROCESSING, "B обробці"),)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    data_create = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=status_choice, default=PROCESSING)
    total_price = models.IntegerField()

    def __str__(self):
        return "{}".format(self.user.username)


class OrderItem(models.Model):
    class Meta:
        db_table = "order_items"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_item")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="order_item")
    qty = models.IntegerField()

    def __str__(self):
        return "{}".format(self.dish)
