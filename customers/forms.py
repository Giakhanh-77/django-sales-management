from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'ten', 'sdt', 'email', 'dia_chi', 'password1', 'password2')
        labels = {
            'ten': 'Tên',
            'sdt': 'Số điện thoại',
            'email': 'Email',
            'dia_chi': 'Địa chỉ',
        }
        
class LoginForm(forms.Form):
    username = forms.CharField(
        label="Tên đăng nhập",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập username'
        })
    )
    password = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nhập mật khẩu'
        })
    )   
