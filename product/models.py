from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30)
    slug=models.SlugField(max_length = 100, null=True, blank=True, unique=True)
    def __str__(self):
        return self.name


class Size(models.Model):
    name=models.CharField(max_length=30)
    slug=models.SlugField(max_length = 100, null=True, blank=True, unique=True)
    def __str__(self):
        return self.name


class Color(models.Model):
    name=models.CharField(max_length=30)
    slug=models.SlugField(max_length = 100, null=True, blank=True, unique=True)
    def __str__(self):
        return self.name


class Product(models.Model):
    title=models.CharField(max_length=30)
    description=models.TextField()
    image=models.ImageField(upload_to='media/',blank=True,null=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.FloatField()

    def __str__(self):
        return self.title

rating=(
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5),
)
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    name=models.CharField(max_length=30)
    email=models.EmailField()
    text=models.TextField()
    rating=models.IntegerField(choices=rating)
    created_on=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review By {self.name}"