from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Order, Customer

class OrderForm(ModelForm) :
    class Meta :
        model = Order
        fields = ['customer', 'product', 'status']
        # fields = '__all__'


class userRegistrationForm(UserCreationForm) :
    class Meta :
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class profileUpdationForm(ModelForm) :
    class Meta :
        model = Customer
        fields = ['name', 'email']