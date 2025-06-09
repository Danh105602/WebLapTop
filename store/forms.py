from django import forms
from django.contrib.auth.models import User
from .models import Product, Category, Order

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        label='Họ và tên',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label='Số điện thoại',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        label='Địa chỉ',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    city = forms.CharField(
        label='Thành phố',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    district = forms.CharField(
        label='Quận/Huyện',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    ward = forms.CharField(
        label='Phường/Xã',
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    note = forms.CharField(
        label='Ghi chú',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    ) 

class UpdateAddressForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address']