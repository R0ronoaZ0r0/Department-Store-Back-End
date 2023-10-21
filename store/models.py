import uuid

from django.db import models


# Create your models here.
class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    department_number = models.PositiveIntegerField(unique=True)
    image = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'department'
        ordering = ['department_number']


class Subcategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True)
    subcategory_number = models.PositiveIntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    image = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'subcategory'
        ordering = ['subcategory_number']


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=True)
    price = models.FloatField(null=False)
    stock_quantity = models.IntegerField(null=False)
    brand = models.CharField(max_length=100, null=True)
    average_rating = models.FloatField(null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=False)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=False)
    image = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'product'
        ordering = ['department']


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    middle_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=100, null=False)
    phone = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=20, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user'
        ordering = ['-created_at']


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30, null=True)
    address_line_1 = models.TextField(null=False)
    address_line_2 = models.TextField(null=False)
    city = models.CharField(max_length=50, null=False)
    state = models.CharField(max_length=50, null=False)
    zipcode = models.CharField(max_length=10, null=False)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'address'
        ordering = ['-created_at']


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, through='CartProduct')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
        ordering = ['-created_at']


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cart_product'
        ordering = ['-created_at']


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, null=False)
    security_code = models.CharField(max_length=3, null=False)
    payment_method_name = models.CharField(max_length=30, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payment'
        ordering = ['-created_at']


class ProductReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    review = models.TextField(null=False)
    rating = models.PositiveIntegerField(null=False, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product_review'
        ordering = ['created_at']


class Promo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    promo_code = models.CharField(max_length=10, null=False)
    percentage = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'promo'
        ordering = ['-created_at']


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, null=True, on_delete=models.DO_NOTHING)
    payment = models.ForeignKey(Payment, null=False, on_delete=models.DO_NOTHING)
    is_pickup = models.BooleanField(default=False)
    total_cost = models.FloatField(null=False)
    promo = models.ForeignKey(Promo, null=True, on_delete=models.DO_NOTHING)
    product = models.ManyToManyField(Product, through='OrderProduct')
    order_number = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'
        ordering = ['-created_at']


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.PositiveIntegerField(null=False)
    cost = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'order_product'
        ordering = ['-created_at']
