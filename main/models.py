from django.conf import settings
from django.db import models
from .choices import BannerLocationEnum


class User(models.Model):
    username = models.CharField(max_length=123)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    avatar = models.ImageField(upload_to='media/avatars', blank=True, null=True)
    address = models.CharField(max_length=255)

    ROLE_CHOICES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('seller', 'Seller'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username


class Category(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return self.title


class Size(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=123)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=123)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='media/product_covers')
    old_price = models.DecimalField(decimal_places=2, max_digits=12)
    new_price = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Storage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.product} --> {self.size}({self.quantity}))'


class ProductBrand(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'brand')

    def __str__(self):
        return f"{self.product} - {self.brand}"


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Basket {self} - {self.user}"


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')  # с id_Basket
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.storage} x {self.quantity}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} ❤️ {self.product}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self} --> {self.user} --> {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.storage} x {self.quantity}"


class Banner(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='media/banner_covers')
    location = models.CharField(max_length=20, choices=BannerLocationEnum.choices)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
