from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Purpose, PropertyType, City, LeadRequest, Property, PropertyImage, Lease,Location

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
        

OWNER_CHOICES = [
    ('Owner', 'Owner'),
    ('Agent', 'Agent'),
    ('Builder', 'Builder'),
]

class LeaseForm(forms.ModelForm):
    owner_name = forms.ChoiceField(
        choices=OWNER_CHOICES,
        label="I am *",
        required=True
    )
    contact_name = forms.CharField(
        required=True,
        label="Contact Name *",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact_number = forms.CharField(
        required=True,
        label="Contact Number *",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    property_type = forms.ModelChoiceField(
        queryset=PropertyType.objects.all(),
        required=True,
        label="Property Type *",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        label="City *",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label="Location",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    new_location = forms.CharField(
        required=False,
        label="Add New Location",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new location if not listed'})
    )
    area = forms.CharField(
        required=True,
        label="Area (sq.ft) *",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    price = forms.DecimalField(
        required=True,
        label="Price *",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    terms_and_conditions = forms.CharField(
        required=False,
        label="Terms and Conditions",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = Lease
        fields = [
            'owner_name', 'contact_name', 'property_type', 'city',
            'location', 'new_location', 'area', 'price', 'contact_number',
            'description', 'terms_and_conditions'
        ]
        

class SellPropertyForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        label="Your Name *",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label="Email *",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    mobile = forms.CharField(
        required=True,
        label="Mobile Number *",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    user_type = forms.ChoiceField(
        required=True,
        label="I am *",
        choices=[('Owner', 'Owner'), ('Agent', 'Agent'), ('Builder', 'Builder')],
        widget=forms.RadioSelect
    )
    purpose = forms.ModelChoiceField(
        queryset=Purpose.objects.filter(name__in=['Sell', 'Rent']),
        required=True,
        label="Purpose *",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    property_type = forms.ModelChoiceField(
        queryset=PropertyType.objects.all(),
        required=True,
        label="Property Type *",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        required=True,
        label="City *",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    location = forms.ModelChoiceField(
        queryset=Location.objects.all(),
        required=False,
        label="Location",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    new_location = forms.CharField(
        required=False,
        label="Add New Location",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new location if not listed'})
    )
    description = forms.CharField(
        required=True,
        label="Property Description *",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    price = forms.IntegerField(
        required=True,
        label="Price *",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    area = forms.IntegerField(
        required=True,
        label="Area (sq.ft) *",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Property
        fields = [
            'description',
            'price',
            'purpose',
            'property_type',
            'city',
            'location',
            'new_location',
            'area'
        ]