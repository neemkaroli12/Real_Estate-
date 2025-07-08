from django import forms
from .models import PropertySearch

class PropertySearchForm(forms.ModelForm):
    class Meta:
        model = PropertySearch
        fields = ['purpose', 'property_type', 'city']
        widgets = {
            'purpose': forms.Select(attrs={'class': 'form-select'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['purpose'].empty_label = "Please select purpose"
        self.fields['property_type'].empty_label = "Please select property type"
        self.fields['city'].empty_label = "Please select city"
