from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_countries import CountryCode
from django_countries.fields import CountryField


# Create your models here.
class Customer(models.Model):

    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)

    #extra fields will come here
    profile_pic = models.ImageField(upload_to='profilePics/', default='default/default.jpg')
    phone_field = models.CharField(max_length=12, blank=False)

    def __str__(self) :
        return self.user.username


class Category (models.Model):
    category_name  = models.CharField(max_length=200)
    def __str__(self):
        return self.category_name

class SaleIn (models.Model):
    sale_in = models.CharField(max_length=10, default='KG')
    def __str__(self):
        return self.sale_in

class Product (models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sale_in = models.ForeignKey('SaleIn', on_delete=models.CASCADE)
    desc = models.TextField()
    price = models.FloatField(default=0.0)
    product_available_count = models.IntegerField(default = 0)
    product_image = models.ImageField(upload_to='images/', default='images/default/unnamed.png')
    
    def __str__(self):
            return self.name

    def get_add_to_cart_url (self):
        return reverse ("core:add-to-cart", kwargs={
            "pk":self.pk
        })


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sale_in = models.ForeignKey('SaleIn', on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}  {self.sale_in} of {self.product.name} for {self.user}"

    def get_total_item_price(self):
        return self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_item_price()


class Order (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    order_id = models.CharField(max_length=100, unique=True, default= None, blank = True, null = True)
    datetime_ofpayment = models.DateTimeField(auto_now_add=True)
    order_delivered = models.BooleanField(default=False)
    order_received = models.BooleanField(default=False)

    razorpay_order_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=500, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=500, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.order_id is None and self.datetime_ofpayment and self.id:
            self.order_id = self.datetime_ofpayment.strftime('PAY@ME%Y%m%dODR') + str(self.id)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} have {self.items.count()} items"

    def get_total_price(self):
        return sum(order_item.get_final_price() for order_item in self.items.all()) 

    def get_total_count(self):
        order = Order.objects.get(pk=self.pk)
        return order.items.count()

class CheckoutAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    Country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username