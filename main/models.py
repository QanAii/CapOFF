from django.db import models


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
    brands = models.ManyToManyField(Brand, through='ProductBrand')
    description = models.TextField(blank=True, null=True)
    cover = models.ImageField(upload_to='media/product_covers')
    old_price = models.DecimalField(decimal_places=2, max_digits=12)
    new_price = models.DecimalField(decimal_places=2, max_digits=12, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Storage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # переименовано с id_product
    size = models.ForeignKey(Size, on_delete=models.CASCADE)  # переименовано с id_size
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} - {self.size.title} : {self.quantity}"


class ProductBrand(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # переименовано с id_Product
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)  # переименовано с id_Brand

    class Meta:
        unique_together = ('product', 'brand')

    def __str__(self):
        return f"{self.product.title} - {self.brand.title}"


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # переименовано с id_User
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Basket {self.id} - {self.user.username}"


class BasketItem(models.Model):  # переименовано с BasketItems (во множественном числе не принято)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='items')  # с id_Basket
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)  # с id_Storage
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.storage.product.title} x {self.quantity}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # с id_User
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # с id_Product

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} ❤️ {self.product.title}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # с id_User
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # исправлено update_at -> updated_at

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')  # с id_Order
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)  # с id_Storage
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.storage.product.title} x {self.quantity}"
