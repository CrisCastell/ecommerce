from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
from PIL import Image
# Create your models here.


def make_thumbnail(image, size):
    img = Image.open(image)
    img.convert('RGB')
    img.thumbnail(size)

    thumb_io = BytesIO()
    img.save(thumb_io, 'JPEG', quality=85)

    thumbnail = File(thumb_io, name=image.name)
    return thumbnail


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=254, null=True)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    # profile_pic = models.ImageField(null=True, blank=True, upload_to='profile-pics', default='default-user.png')
    joined_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    # def save(self, *args, **kwargs):
    #     self.thumbnail = make_thumbnail(self.profile_pic, (50, 50))

    #     super().save(*args, **kwargs)






class Product(models.Model):
    CATEGORY_CHOICES = [
        ('N', 'New'),
        ('D', 'Discounts'),
        ('BS', 'Best-Sellers')
    ]
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, null=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(blank=True, null=True , default='https://images.unsplash.com/photo-1509668521827-dd7d42a587e2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60')
    # image = models.ImageField(blank=True, null=True ,upload_to='products', default='no-image.jpg')
    # thumbnail = models.ImageField(null=True, blank=True, upload_to='products', default='no-image-thumbnail.jpg')


    # def save(self, *args, **kwargs):
    #     if self.image and self.image != 'no-image.jpg':
    #         self.thumbnail = make_thumbnail(self.image, (300, 200))

    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    #image = models.ImageField(upload_to='products')
    image = models.URLField(blank=True, null=True )


class SlideProduct(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, blank=True, null=True)

    

class Order(models.Model):
    customer = models.ForeignKey(Customer, blank=True, null=True, on_delete=models.SET_NULL, related_name='orders')
    created_date = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction = models.IntegerField()

    def __str__(self):
        return f"Order: {self.transaction} - {self.customer.username}"

    @property
    def get_cart_items(self):
        items = self.item_set.all()
        total = sum([item.quantity for item in items])

        return total


    @property
    def get_cart_total(self):
        items = self.item_set.all()
        total = sum([item.get_total for item in items])

        return total

   



class Item(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True , on_delete=models.SET_NULL)
    order =  models.ForeignKey(Order, blank=True, null=True , on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    added_date = models.DateField(auto_now_add=True)
    size = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.product} - {self.quantity} - ({self.order})"
    @property
    def get_total(self):
        total = self.quantity * self.product.price

        return total
    
    def serialize(self):
        return {
            "productName":self.product.name,
            "quantity":self.quantity
        }


class Shipping(models.Model):
    order =  models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True ,)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, null=True)

    delivered = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.address
    
    def serialize(self):
        return {
            "shippingId":self.id,
            "address":self.address,
            "city":self.city,
            "state":self.state,
            "zip_code":self.zip_code,
            "date":self.created_date
        }