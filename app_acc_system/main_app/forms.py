from django import forms
from .models import Applications
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
