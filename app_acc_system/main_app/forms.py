from django import forms
from django.core.exceptions import ValidationError

from .models import Applications, ApplicationComments
from client_app.models import Clients


class ApplicationsForms(forms.ModelForm):
    class Meta:
        model = Applications
        fields = ['contact_person', 'contract', 'equipment', 'subject', 'description', 'priority', 'type']
        widgets = {
            'contact_person': forms.Select(attrs={'class': 'form-control'}),
            'contract': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }

    equipment = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    def __init__(self, client_id=None, *args, **kwargs):
        super(ApplicationsForms, self).__init__(*args, **kwargs)
        if client_id:
            client = Clients.objects.prefetch_related('contact_persons', 'equipments', 'contracts').get(pk=client_id)
            self.fields['contact_person'].choices = [
                (item.pk, item.get_full_name) for item in client.contact_persons.all()
            ]
            self.fields['contract'].choices = [(item.pk, item.title) for item in client.contracts.all()]
            self.fields['equipment'].queryset = client.equipments.all()


class ApplicationCommentsForms(forms.ModelForm):
    class Meta:
        model = ApplicationComments
        fields = ['comment_body', 'is_private', 'is_public', 'file']
        widgets = {
            'comment_body': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Введите ваш комментарий...'}
            ),
            'file': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        is_private = self.cleaned_data['is_private']
        is_public = self.cleaned_data['is_public']
        if is_private and is_public:
            raise ValidationError('Выберите только один статус (Публичный или приватный).')
