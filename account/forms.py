from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User
class SignupForm(UserCreationForm):
    class Meta:
        model=User
        fields=('email','password1','password2','name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model=User
        fields=('email','avatar','name')