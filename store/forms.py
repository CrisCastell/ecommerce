from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class UpdateCustomerForm(ModelForm):
    class Meta:
        className='input'
        model = Customer
        fields = '__all__'
        exclude = ['user', 'created_date']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':className}),
            'last_name': forms.TextInput(attrs={'class':className}),
            'email': forms.TextInput(attrs={'class':className}),
            'phone':forms.TextInput(attrs={'class':className}),
            'bio':forms.Textarea(attrs={'class':className}),
            'profile_pic':forms.FileInput(attrs={'class':className}),
        }