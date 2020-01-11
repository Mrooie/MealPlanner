from django.contrib.auth.models import User
from django import forms
from django.core.validators import validate_email


class LoginForm(forms.Form):
    username = forms.CharField(label="Your username", max_length=255, required=True)
    password = forms.CharField(label="Your password", widget=forms.PasswordInput, max_length=255, required=True)


class UserRegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    class Meta:
        fields = ("username", "first_name", "last_name", "email", "password")
        model = User
        widgets = {"password": forms.PasswordInput}
        validators = {"email": [validate_email]}
        help_texts = {
            'username': 'Letters, digits and @/./+/-/_ only.',
        }


class ResetPasswordForm(forms.Form):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
