from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm

from authtools import forms as authforms


User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )

    class Meta:
        model = User
        fields = ('username', 'password')


class SignUpForm(authforms.UserCreationForm):

    email = forms.CharField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'E-mail'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': 'Verify password'})
    )

    class Meta:
        model = User
        fields = ('email',)
