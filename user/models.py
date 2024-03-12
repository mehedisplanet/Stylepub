from django.db import models
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.
class ContactUs(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    phone=models.IntegerField(null=True)
    body=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email By {self.email}"
    class Meta:
        verbose_name_plural='Contact Us'


class Purchase(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    purchase_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    purchase_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username
    



class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


