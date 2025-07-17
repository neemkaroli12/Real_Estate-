from django.shortcuts import render, get_object_or_404, redirect
from .models import Property, Purpose, City, newProject, PropertyImage, LeadRequest
from .forms import PropertySearchForm, LeadRequestForm,PropertyForm,CustomUserCreationForm
from django.conf import settings
import requests
import random
from .utils import send_otp, generate_otp
from django.contrib.auth.decorators import login_required


# Home page with search and project list
def home(request):
    form = PropertySearchForm(request.GET or None)
    results = None
    projects = newProject.objects.all()

    if form.is_valid():
        purpose = form.cleaned_data['purpose']
        property_type = form.cleaned_data['property_type']
        city = form.cleaned_data['city']

        # Auto-map "Buy" to "Sell"
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


# View properties for Buy
def buy_properties(request):
    try:
        sell_purpose = Purpose.objects.get(name__iexact="Sell")
        properties = Property.objects.filter(purpose=sell_purpose, is_approved=True).order_by('-id')
    except Purpose.DoesNotExist:
        properties = Property.objects.none()
    return render(request, 'buy.html', {'properties': properties})



# View properties for Rent
def rent_properties(request):
    try:
        rent_purpose = Purpose.objects.get(name__iexact="Rent")
        properties = Property.objects.filter(purpose=rent_purpose, is_approved=True).order_by('-id')
    except Purpose.DoesNotExist:
        properties = Property.objects.none()
    return render(request, 'rent.html', {'properties': properties})



# View properties for Lease
def lease_properties(request):
    try:
        lease_purpose = Purpose.objects.get(name__iexact="Lease")
        properties = Property.objects.filter(purpose=lease_purpose, is_approved=True).order_by('-id')
    except Purpose.DoesNotExist:
        properties = Property.objects.none()
    return render(request, 'lease.html', {'properties': properties})


# City detail to show locations and grouped properties
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


# Property detail page with contact modal and lead form
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



# OTP verification view (mock OTP = 123456)
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
    
    # For debugging (optional)
    print("SMS response:", response.text)

    return otp


@login_required(login_url='user-login')

def post_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property_obj = form.save(commit=False)

            # Auto title (optional)
            property_obj.title = f"{form.cleaned_data['property_type']} in {form.cleaned_data['location']}"
            property_obj.posted_by = request.user
            property_obj.is_approved = False
            property_obj.save()

            # Handle images
            images = request.FILES.getlist('images')
            for img in images:
                PropertyImage.objects.create(property=property_obj, image=img)

            return render(request, 'property_submitted.html', {'property': property_obj})
        else:
            print("Form errors:", form.errors)  # 🔍 check in terminal
    else:
        form = PropertyForm()

    return render(request, 'post_property.html', {'form': form})
 

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-login')  # After signup go to login
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # or email if using email as username
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  # change 'home' to your desired redirect after login
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('user-login')
