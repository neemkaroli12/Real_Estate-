from django import forms
from .models import Purpose, PropertyType, City, LeadRequest

class PropertySearchForm(forms.Form):
    purpose = forms.ModelChoiceField(
        queryset=Purpose.objects.all(),
        empty_label="Please select purpose",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    property_type = forms.ModelChoiceField(
        queryset=PropertyType.objects.all(),
        empty_label="Please select property type",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Please select city",
        widget=forms.Select(attrs={'class': 'form-select'})
    )



class LeadRequestForm(forms.ModelForm):
    class Meta:
        model = LeadRequest
        fields = ['name', 'email', 'whatsapp']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'whatsapp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'WhatsApp Number',
                'pattern': '[0-9]{10}',
                'title': 'Enter 10-digit WhatsApp number'
            }),
        }