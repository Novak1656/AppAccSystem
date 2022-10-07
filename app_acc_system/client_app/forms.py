from django import forms
from django.core.exceptions import ValidationError
import requests
from .models import Clients, ClientFiles, ContactPersons, Contracts, ContractFiles, EquipmentType, EquipmentAttribute, \
    Equipments, EquipmentFiles
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
        try:
            resp = requests.head(site_url)
            if resp.status_code == 404:
                raise ValidationError('Указаный адрес сайта не действителен')
            return site_url
        except Exception:
            raise ValidationError('Указаный адрес сайта не действителен')


class ClientFilesForms(forms.ModelForm):
    class Meta:
        model = ClientFiles
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ContactPersonsForms(forms.ModelForm):
    class Meta:
        model = ContactPersons
        fields = ['first_name', 'second_name', 'last_name', 'post', 'email', 'phone', 'note']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'second_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'post': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': PhoneNumberPrefixWidget(initial='RU', attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ContractsForms(forms.ModelForm):
    class Meta:
        model = Contracts
        fields = ['title', 'price', 'note']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'})
        }


class ContractsFilesForms(forms.ModelForm):
    class Meta:
        model = ContractFiles
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }


class EquipmentTypeForms(forms.ModelForm):
    class Meta:
        model = EquipmentType
        fields = ['code', 'name']
        widgets = {
            'code': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class EquipmentAttributeForms(forms.ModelForm):
    class Meta:
        model = EquipmentAttribute
        fields = ['code', 'name', 'type_e', 'type_a']
        widgets = {
            'code': forms.NumberInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type_a': forms.Select(choices=EquipmentAttribute.ATTRS_TYPES, attrs={'class': 'form-control'}),
        }

    type_e = forms.ModelMultipleChoiceField(
        queryset=EquipmentType.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )


class EquipmentsForms(forms.ModelForm):
    class Meta:
        model = Equipments
        fields = ['name', 'type', 'note']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control'})
        }


class EquipmentFilesForm(forms.ModelForm):
    class Meta:
        model = EquipmentFiles
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }
