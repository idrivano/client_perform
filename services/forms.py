from django import forms
from django.db.models import Q

from .models import *


class ClientForm(forms.ModelForm):
    STATUS_CHOICES = [
        (1, 'Activate'),
        (0, 'Disabled')
    ]

    first_name = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'Prenom')
    last_name = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'Nom')
    email = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'email',
    }), label = 'Email')
    phone_number = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control ps-0', 'type' : 'text',
    }), label = 'Phone Number', required=False)
    status = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-select'
    }), choices=STATUS_CHOICES, label="Status", initial=1)

    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'status']

class AdressForm(forms.ModelForm):
    zip = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'BP', required=False)
    road = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'Rue', required=False)
    district = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'Quartier', required=False)
    city = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'Ville', required=False)
    state = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'Région', required=False)
    country = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'Pays', required=False)
    
    class Meta:
        model = Address
        fields = ['zip', 'road', 'district', 'city', 'state', 'country']


class ProductForm(forms.ModelForm):
    title = forms.CharField(widget = forms.TextInput(attrs = {
        'class' : 'form-control', 'type' : 'text',
    }), label = 'Nom Produit')
    desc = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'form-control', 'type' : 'text',
    }), label='Description')
    price = forms.DecimalField(widget = forms.NumberInput(attrs = {
        'class' : 'form-control', 'type' : 'number',
    }), label = 'Prix')
    stock = forms.IntegerField(widget = forms.NumberInput(attrs = {
        'class' : 'form-control', 'type' : 'number',
    }), label = 'Quantité')

    class Meta:
        model = Product
        fields = ['title', 'desc', 'price', 'stock']

