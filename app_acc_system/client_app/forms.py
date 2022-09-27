from django import forms
from django.core.exceptions import ValidationError
import requests
from .models import Clients
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class ClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['name', 'second_name', 'site', 'email', 'phone',
                  'office_address', 'legal_address', 'inn', 'kpp', 'ogrn', 'note']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': PhoneNumberPrefixWidget(initial='RU', attrs={'class': 'form-control'}),
            'office_address': forms.TextInput(attrs={'class': 'form-control'}),
            'legal_address': forms.TextInput(attrs={'class': 'form-control'}),
            'inn': forms.TextInput(attrs={'class': 'form-control'}),
            'kpp': forms.TextInput(attrs={'class': 'form-control'}),
            'ogrn': forms.TextInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean_inn(self):
        inn = self.cleaned_data['inn']
        if not inn.isdigit():
            raise ValidationError('ИНН должен состоять только из цифр')
        return inn

    def clean_kpp(self):
        kpp = self.cleaned_data['kpp']
        if not kpp.isdigit():
            raise ValidationError('КПП должен состоять только из цифр')
        return kpp

    def clean_ogrn(self):
        ogrn = self.cleaned_data['ogrn']
        if not ogrn.isdigit():
            raise ValidationError('ОГРН должен состоять только из цифр')
        return ogrn

    def clean_site(self):
        site_url = self.cleaned_data['site']
        resp = requests.head(site_url)
        if resp.status_code == 404:
            raise ValidationError('Указаный адрес сайта не действителен')
        return site_url