from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from uuid import uuid4


class Collection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Product(models.Model):
    
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    cover_image = models.ImageField(upload_to='store/images')


    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="images")
    image = models.ImageField(upload_to='store/images')

class Customer(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE,'Male'),
        (FEMALE,'Female')
    ]

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES,null=True,blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'B'
    PAYMENT_STATUS_COMPLETE = 'A'
    PAYMENT_STATUS_FAILED = 'C'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT,related_name="orders")


    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]

class CustomOrder(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    left_side_image = models.ImageField()
    right_side_image = models.ImageField()
    front_image = models.ImageField()
    rear_image = models.ImageField()
    placed_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.product_name
    def order(self):
        return f"Custom Order {self.id}"
    def ordered_by(self):
        return self.customer.user.first_name + self.customer.user.last_name 
    

class WishList(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class WishListItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    wishlist = models.ForeignKey(WishList,on_delete=models.CASCADE, related_name='items')


