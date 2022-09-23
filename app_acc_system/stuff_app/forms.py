from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import StuffUsers


class StuffUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль...'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль ещё раз...'})
    )

    class Meta:
        model = StuffUsers
        fields = [
            'username', 'first_name', 'second_name', 'last_name',
            'role', 'email', 'phone', 'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин...'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию...'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя...'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество (при наличии)...'}),
            'role': forms.Select(choices=StuffUsers.ROLES, attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Введите email...'}),
            'phone': PhoneNumberPrefixWidget(initial='RU', attrs={'class': 'form-control', 'placeholder': '79*********'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError('Пароли не совпадают')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class StuffUserInfoForm(forms.ModelForm):
    class Meta:
        model = StuffUsers
        fields = ('first_name', 'second_name', 'last_name', 'role', 'email', 'phone',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(choices=StuffUsers.ROLES, attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': PhoneNumberPrefixWidget(initial='RU', attrs={'class': 'form-control'})
        }


class StuffUserLoginChangeForm(forms.ModelForm):
    class Meta:
        model = StuffUsers
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите новый логин...'}),
        }


class StuffUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите логин...'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput({'class': 'form-control', 'placeholder': 'Введите пароль...'})
    )
