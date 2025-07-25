from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import requests
import random
from django.http import JsonResponse
from .models import  Property, Purpose, City, newProject, PropertyImage, LeadRequest,PropertyType, Location, Lease, LeaseImage
from .forms import PropertySearchForm, LeadRequestForm, PropertyForm, CustomUserCreationForm,  SellPropertyForm, LeaseForm
from .utils import send_otp, generate_otp
from django.http import HttpResponseForbidden

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
        properties = Property.objects.filter(purpose=sell_purpose, is_approved=True).prefetch_related('images').order_by('-id')
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


@login_required(login_url='user-login')
@login_required(login_url='user-login')
def post_lease(request):
    if request.method == 'POST':
        form = LeaseForm(request.POST, request.FILES)
        if form.is_valid():
            lease = form.save(commit=False)
            lease.owner_user = request.user

            # Handle new location
            new_location_name = form.cleaned_data.get('new_location')
            selected_location = form.cleaned_data.get('location')

            if new_location_name and not selected_location:
                city = form.cleaned_data.get('city')
                selected_location, _ = Location.objects.get_or_create(name=new_location_name, city=city)
                lease.location = selected_location
            else:
                lease.location = selected_location

            lease.save()

            for image in request.FILES.getlist('images'):
                LeaseImage.objects.create(lease=lease, image=image)
            return redirect('lease_properties')
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

@login_required
def edit_lease(request, pk):
    lease = get_object_or_404(Lease, pk=pk)

    if request.user != lease.owner_user:
        return HttpResponseForbidden("You are not allowed to edit this lease.")

    if request.method == 'POST':
        form = LeaseForm(request.POST, request.FILES, instance=lease)
        if form.is_valid():
            lease = form.save()
            images = request.FILES.getlist('images')
            for img in images:
                LeaseImage.objects.create(lease=lease, image=img)
            return redirect('lease_properties')
        else:
            print("Form errors:", form.errors)
    else:
        form = LeaseForm(instance=lease)

    return render(request, 'edit_lease.html', {'form': form, 'lease': lease})

@login_required
def delete_lease(request, pk):
    lease = get_object_or_404(Lease, pk=pk)

    if request.user != lease.owner_user:
        return HttpResponseForbidden("You are not allowed to delete this lease.")

    if request.method == 'POST':
        lease.delete()
        return redirect('lease_properties')

    return render(request, 'delete_confirm.html', {'lease': lease})


# projects 
def newprojects(request):
    projects = newProject.objects.all()
    
    for project in projects:
        if project.brochure and project.brochure.url.lower().endswith(".pdf"):
            project.fixed_brochure_url = project.brochure.url.replace("/image/upload/", "/raw/upload/")
        else:
            project.fixed_brochure_url = None
    
    return render(request, "projects.html", {"projects": projects})


#  Sell Form View
@login_required(login_url='user-login')
def sell_property_view(request):
    if request.method == 'POST':
        form = SellPropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.posted_by = request.user

            new_location_name = form.cleaned_data.get('new_location')
            selected_location = form.cleaned_data.get('location')

            if new_location_name and not selected_location:
                city = form.cleaned_data.get('city')
                selected_location, _ = Location.objects.get_or_create(name=new_location_name, city=city)

            property_instance.location = selected_location
            property_instance.save()

            images = request.FILES.getlist('images')
            for img in images:
                PropertyImage.objects.create(property=property_instance, image=img)

            return redirect('buy_properties')
    else:
        form = SellPropertyForm()

    context = {
        'form': form,
        'purposes': form.fields['purpose'].queryset,
        'property_types': form.fields['property_type'].queryset,
        'cities': form.fields['city'].queryset,
        'locations': Location.objects.all()
    }
    return render(request, 'sell_form.html', context)

# about 
def about(request):
    return render(request, "about.html")
# services
def service(request):
    return render(request,"services.html")
