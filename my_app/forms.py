from django import forms
from .models import Purpose, PropertyType, City

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
