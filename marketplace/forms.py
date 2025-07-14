from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'student_id', 'ghana_card_number', 'school', 'profile_image', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Phone')    
