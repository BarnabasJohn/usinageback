from django.db import models
from django.contrib.auth.models import AbstractUser
from client.models import Request2, Client
from manufacturer.models import Manufacturer, Offer
from cloudinary.models import CloudinaryField

# Create your models here.
class Admin(AbstractUser):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.CharField(max_length=255, unique=True, null=False)
    password1 = models.CharField(max_length=255, blank=False)
    password2 = models.CharField(max_length=255, blank=False)
    created = models.DateTimeField(auto_now_add=True)

    username = models.CharField(max_length=100, null=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = "Admin"
        verbose_name_plural = "Admins"

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='admin_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='admin_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.first_name
    

class News(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    #image = models.ImageField(upload_to='news-images/', blank=True, null=True)
    image = CloudinaryField('image', folder='news-images', blank=True, null=True)
    tags = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    article = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
    
class Contact(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    company = models.CharField(max_length=200, null=True, blank=True)
    Phone = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=True, blank=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name
    
class ClientFAQ(models.Model):
    question = models.CharField(max_length=200, null=False, blank=False)
    tags = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.question
    

class ManFAQ(models.Model):
    question = models.CharField(max_length=200, null=False, blank=False)
    tags = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    answer = models.TextField(null=False, blank=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.question
    

class ClientPayment(models.Model):
    request = models.ForeignKey(Request2, on_delete=models.SET_NULL, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=200,null=False, blank=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = "ClientPayment"
        verbose_name_plural = "ClientPayments"

    def __str__(self):
        return self.request.title
    

class ManufacturerWithdrawal(models.Model):
    request = models.ForeignKey(Request2, on_delete=models.SET_NULL, null=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    offer = models.ForeignKey(Offer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.CharField(max_length=200,null=False, blank=False)
    paid = models.BooleanField(default=False)
    payment_requested = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = "ManufacturerWithdrawal"
        verbose_name_plural = "ManufacturerWithdrawals"

    def __str__(self):
        return self.request.title