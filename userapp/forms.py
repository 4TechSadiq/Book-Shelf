from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email",)
        widgets = widgets = {
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }),
            "password1": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your password"
            }),
            "password2": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder": "Confirm your password"
            }),
        }


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)
        widgets = {
            "Email address": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder":"enter the title"
            }),
            "Password": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder":"enter the Price"
            }),
            "Password confirmation": forms.PasswordInput(attrs={
                "class": "form-control",
                "placeholder":"enter the price"
            }),
        }