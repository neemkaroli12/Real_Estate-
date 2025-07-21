from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests
import random
from django.http import JsonResponse
from .models import  Property, Purpose, City, newProject, PropertyImage, LeadRequest, Lease , PropertyType, Location, LeaseImage
from .forms import PropertySearchForm, LeadRequestForm, PropertyForm, CustomUserCreationForm, LeaseForm
from .utils import send_otp, generate_otp
from django.http import JsonResponse

# ======================= Home & Search =======================

def home(request):
    form = PropertySearchForm(request.GET or None)
    results = None
    projects = newProject.objects.all()

    if form.is_valid():
        purpose = form.cleaned_data['purpose']
        property_type = form.cleaned_data['property_type']
        city = form.cleaned_data['city']

        if purpose.name.lower() == "buy":
            try:
                purpose = Purpose.objects.get(name__iexact="Sell")
            except Purpose.DoesNotExist:
                purpose = None

        results = Property.objects.filter(
            purpose=purpose,
            property_type=property_type,
            city=city
        )

        return render(request, 'output.html', {
            'result': results,
        })

    return render(request, 'index.html', {
        'form': form,
        'projects': projects
    })


# ======================= Property Listings =======================

def buy_properties(request):
    try:
        sell_purpose = Purpose.objects.get(name__iexact="Sell")
        properties = Property.objects.filter(purpose=sell_purpose, is_approved=True).order_by('-id')
    except Purpose.DoesNotExist:
        properties = Property.objects.none()
    return render(request, 'buy.html', {'properties': properties})


def rent_properties(request):
    try:
        rent_purpose = Purpose.objects.get(name__iexact="Rent")
        properties = Property.objects.filter(purpose=rent_purpose, is_approved=True).order_by('-id')
    except Purpose.DoesNotExist:
        properties = Property.objects.none()
    return render(request, 'rent.html', {'properties': properties})


def lease_properties(request):
    properties = Lease.objects.all().order_by('-id')
    return render(request, 'lease.html', {'properties': properties})


# ======================= City & Property Details =======================

def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    locations = city.locations.all()

    location_properties = []
    for location in locations:
        properties = Property.objects.filter(location=location)
        if properties.exists():
            location_properties.append({
                'location': location,
                'properties': properties
            })

    return render(request, 'city_detail.html', {
        'city': city,
        'location_properties': location_properties
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    related_properties = Property.objects.filter(city=property_obj.city).exclude(pk=pk)[:3]
    lead_form = LeadRequestForm()

    if request.method == 'POST' and 'lead_form_submit' in request.POST:
        lead_form = LeadRequestForm(request.POST)
        if lead_form.is_valid():
            lead = lead_form.save(commit=False)
            lead.property = property_obj

            otp = generate_otp()
            lead.otp = otp
            lead.save()

            phone = '91' + lead.whatsapp
            send_otp(phone, otp)

            request.session['lead_id'] = lead.id
            return redirect('verify_otp', pk=pk)

    return render(request, 'property_detail.html', {
        'property': property_obj,
        'lead_form': lead_form,
        'related_properties': related_properties
    })


# ======================= OTP Verification =======================

def verify_otp_view(request, pk):
    lead_id = request.session.get('lead_id')
    lead = get_object_or_404(LeadRequest, id=lead_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == lead.otp:
            lead.is_verified = True
            lead.save()
            return render(request, 'otp_success.html', {
                'lead': lead,
                'property': lead.property
            })
        else:
            return render(request, 'verify_otp.html', {
                'property': lead.property,
                'error': 'Invalid OTP'
            })

    return render(request, 'verify_otp.html', {'property': lead.property})


def send_sms_otp(phone_number):
    otp = str(random.randint(100000, 999999))
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        'variables_values': otp,
        'route': 'otp',
        'numbers': phone_number
    }
    headers = {
        'authorization': settings.FAST2SMS_API_KEY,
        'Content-Type': "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)
    print("SMS response:", response.text)
    return otp


# ======================= Post Property =======================
@login_required(login_url='user-login')
def post_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)

            # Get Purpose
            purpose_name = request.POST.get('purpose')
            try:
                purpose = Purpose.objects.get(name__iexact=purpose_name)
                property_obj.purpose = purpose
            except Purpose.DoesNotExist:
                messages.error(request, 'Invalid purpose selected.')
                return render(request, 'post_property.html', {'form': form})

            # Get Property Type
            property_type_name = request.POST.get('property_type')
            try:
                property_type = PropertyType.objects.get(name__iexact=property_type_name)
                property_obj.property_type = property_type
            except PropertyType.DoesNotExist:
                messages.error(request, 'Invalid property type selected.')
                return render(request, 'post_property.html', {'form': form})

            # Get City
            city_name = request.POST.get('city')
            try:
                city = City.objects.get(name__iexact=city_name)
                property_obj.city = city
            except City.DoesNotExist:
                messages.error(request, 'Invalid city selected.')
                return render(request, 'post_property.html', {'form': form})

            # Get Location
            location_name = request.POST.get('location')
            try:
                location = Location.objects.get(name__iexact=location_name, city=city)
                property_obj.location = location
            except Location.DoesNotExist:
                messages.error(request, 'Invalid location selected.')
                return render(request, 'post_property.html', {'form': form})

            # Final save
            property_obj.title = f"{property_type.name} in {location.name}"
            property_obj.posted_by = request.user
            property_obj.is_approved = False
            property_obj.save()

            # Save Images
            images = request.FILES.getlist('images')
            for img in images:
                PropertyImage.objects.create(property=property_obj, image=img)

            return render(request, 'property_submitted.html', {'property': property_obj})
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PropertyForm()

    return render(request, 'post_property.html', {'form': form})

# ------------ Authentication ---------------

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Signed up')
            return redirect('user-login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in')
            return redirect('buy_properties')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('user-login')

# -----Post lease -------
@login_required(login_url='user-login')
def post_lease(request):
    if request.method == 'POST':
        form = LeaseForm(request.POST)
        if form.is_valid():
            lease = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                LeaseImage.objects.create(lease=lease, image=image)
            return redirect('lease_properties')  # URL name of listing page
    else:
        form = LeaseForm()
    return render(request, 'post_lease.html', {'form': form})

def lease_properties(request):
    properties = Lease.objects.filter(is_approved=True).prefetch_related('images').order_by('-id')
    return render(request, 'lease.html', {'properties': properties})

def load_locations(request):
    city_id = request.GET.get('city_id')
    locations = Location.objects.filter(city_id=city_id).values('id', 'name')
    return JsonResponse(list(locations), safe=False)


def edit_lease(request, pk):
    lease = get_object_or_404(Lease, pk=pk)
    if request.method == 'POST':
        form = LeaseForm(request.POST, instance=lease)
        if form.is_valid():
            form.save()
            return redirect('lease_properties')
    else:
        form = LeaseForm(instance=lease)
    return render(request, 'edit_lease.html', {'form': form, 'lease': lease})


def delete_lease(request, pk):
    lease = get_object_or_404(Lease, pk=pk)
    if request.method == 'POST':
        lease.delete()
        return redirect('lease_properties')
    return render(request, 'delete_confirm.html', {'lease': lease})

# projects 
def newprojects(request):
    projects = newProject.objects.all()  # or apply filters if needed
    return render(request, 'projects.html', {'projects': projects})
