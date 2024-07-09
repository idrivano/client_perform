from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission

from .manager import UserManager


# Create your models here.
class Role(models.Model):
    status = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status

class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='services_user_groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='services_user_permissions'
    )

    email = models.EmailField(unique=True, null=True)
    indicatif = models.CharField(max_length=7, default="+228")
    phone_number = models.CharField(max_length=24, unique=True)
    profile = models.FileField(upload_to="profile/", blank=True)
    role = models.ForeignKey('Role', on_delete=models.CASCADE, default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
    
class Client(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=True)
    indicatif = models.CharField(max_length=7, default="+228")
    phone_number = models.CharField(max_length=24, unique=True)
    status = models.BooleanField(default=True)
    profile = models.FileField(upload_to="clients/", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Address(models.Model):
    zip = models.CharField(max_length=255, blank=True)
    road = models.CharField(max_length=255, blank=True)
    district = models.CharField(max_length=255, blank=False)
    state = models.CharField(max_length=255, blank=False)
    city = models.CharField(max_length=255, blank=False)
    country = models.CharField(max_length=255, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Client, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.client.email
    
class Product(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    price = models.FloatField(default=0)
    thumbnail = models.FileField(upload_to="products/")
    stock = models.IntegerField(default=0, null=True)
    stock_max = models.IntegerField(default=0, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title[:25]
       
class Order(models.Model):
    quantity = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.email
    
class Service(models.Model):
    desc = models.TextField(blank=True)
    image = models.FileField(upload_to='service/')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.email

class Support(models.Model):
    time = models.TimeField(blank=True)
    desc = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.email
    
class Evaluation(models.Model):
    loyalty_score = models.IntegerField(default=0)
    purchases_score = models.IntegerField(default=0)
    services_score = models.IntegerField(default=0)
    engagement_score = models.IntegerField(default=0)
    overall_score = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.email

class Task(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.client.email