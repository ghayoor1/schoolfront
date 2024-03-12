from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.forms.widgets import PasswordInput, TextInput
from . models import Customer, Contact


# - Register/Create a user

class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ["username","password1","password2"]

# - Login a user

class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

# - Add a record
    
class AddRecordForm(forms.ModelForm):
        class Meta:

            model = Customer
            fields = ["first_name","last_name","country"]

# - Update a record
    
class UpdateRecordForm(forms.ModelForm):
        class Meta:

            model = Customer
            fields = ["first_name","last_name","country"]

# - Add a contact
    
class AddContactForm(forms.ModelForm):
        username = forms.CharField(max_length=150)
        class Meta:

            model = Contact
            fields = ["username"]
           


