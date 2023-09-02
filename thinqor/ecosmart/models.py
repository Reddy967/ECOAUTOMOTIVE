from django.db import models

# Create your models here.

class Register(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=20)
    password = models.CharField(max_length=100)


class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='static/images')
    amount = models.FloatField()

class Product_Book(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class Product_Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)


class ShippingAddress(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)

class Checkout(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.FloatField()


class Checkout_Cart(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user_shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.FloatField()


class DiscountCoupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    amount = models.FloatField()


class Payment(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    total_amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100)
    razorpay_payment_status = models.CharField(max_length=100)
    razorpay_payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

STATUS_CHOICES = [
        ('Accepted', 'Accepted'),
        ('Packed', 'Packed'),
        ('On The Way', 'On The Way'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Pending', 'Pending'),
    ]



class OrderPlaced(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.ForeignKey(Checkout, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)




