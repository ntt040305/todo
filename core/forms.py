from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Todo


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Nhập công việc...',
                'class': 'form-input'
            })
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tên đăng nhập'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mật khẩu'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nhập lại mật khẩu'})
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email này đã được sử dụng')
        return email


