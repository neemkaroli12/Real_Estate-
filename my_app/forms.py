from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Purpose, PropertyType, City, LeadRequest, Property, PropertyImage,Lease, Location

# Property Search Filter Form
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

# Lead Inquiry Form
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

# Property Submission Form
class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'description', 'price', 'purpose', 'property_type',
            'city', 'location', 'area', 'facing', 'ownership',
            'transaction_type', 'agent_phone', 'brochure', 'is_approved'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'purpose': forms.Select(attrs={'class': 'form-select'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'location': forms.Select(attrs={'class': 'form-select'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'facing': forms.TextInput(attrs={'class': 'form-control'}),
            'ownership': forms.TextInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.TextInput(attrs={'class': 'form-control'}),
            'agent_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'brochure': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_approved': forms.CheckboxInput(),
        }

# Property Image Upload Form
class PropertyImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image', widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PropertyImage
        fields = ['image']

# Custom User Registration Form
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class LeaseForm(forms.ModelForm):
    # images = forms.ImageField(
    #     widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}),
    #     required=False
    # )

    class Meta:
        model = Lease
        fields = ['city', 'location', 'area', 'price', 'contact_name', 'contact_number', 'description']
