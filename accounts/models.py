from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model) :
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


    def __str__(self) :
        return self.name

class Tag(models.Model) :
    # TAGS
    name = models.CharField(max_length=100, null=True)

    def __str__(self) :
        return self.name


class Product(models.Model) :
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
    )


    name = models.CharField(max_length=100, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=100, null=True, choices=CATEGORY)
    description = models.TextField(max_length=100, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self) :
        return self.name


class Order(models.Model) :
    STATUS = (
        ('Pending', 'Pending'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)

    # actually, product to order is a ManyToMany relationship because one order can have many products and
        # one product can be in multiple orders
    # but in this project, I assumed that one order can have only one product to be ordered,
        # so, I gave them OneToMany relationship
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    status = models.CharField(max_length=100, null=True, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)

    note = models.CharField(max_length=100, null=True, blank=False)

    def __str__(self) :
        # return str(self.customer) + ", " + str(self.date_created)
        return self.customer.name + ", " + str(self.date_created)