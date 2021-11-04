from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from commerce.models import Product
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'