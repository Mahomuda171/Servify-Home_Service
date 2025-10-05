from django.shortcuts import render, redirect,get_object_or_404
from .blog_form import BlogForm
from django.contrib.auth.decorators import login_required,user_passes_test
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileUpdateForm, WorkerProfileUpdateForm
from django.contrib.auth import authenticate,logout, login as auth_login
from .models import Blog
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Service, SubService, WorkerProfile, User, Booking
from .forms import BookingForm  # We'll create this next
from .models import SubService
from .models import Service, SubService
from .models import Service, SubService, WorkerProfile
from django.http import Http404




# Home page
def home(request):
    return render(request, 'landing_page/home.html')


# Signup page
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # Redirect based on user type
            if user.user_type == 'worker':
                return redirect('login')
            else:
                return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'landing_page/signup.html', {'form': form})

# Login page - FIXED
def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)  # This is correct - request and user
                # Redirect based on user type
                if user.user_type == 'worker':
                    return redirect('worker_profile')
                else:
                    return redirect('customer_profile')
    else:
        form = CustomAuthenticationForm()
    # FIX: Use login.html template instead of signup.html
    return render(request, 'landing_page/login.html', {'form': form})


@login_required
def worker(request):
    return render(request, 'worker_dashboard/worker.html')
# About page
def about(request):
    return render(request, 'landing_page/about.html')

# FAQ page
def faq(request):
    return render(request, 'landing_page/faq.html')
# Blog page
def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'landing_page/blog.html', {'blogs': blogs})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog')  # Fix the redirect
    else:
        form = BlogForm()
    return render(request, 'landing_page/create_blog.html', {'form': form})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_response(request, blog_id):
    blog = get_object_or_404(Blog, blog_id=blog_id)

    if request.method == 'POST':
        admin_response = request.POST.get('admin_response')
        contacted = request.POST.get('contacted') == 'on'

        blog.admin_response = admin_response
        blog.contacted = contacted
        blog.save()
        return redirect('blog')

    return render(request, 'landing_page/admin_response.html', {'blog': blog})


# Services page (lists all services)
def service(request):
    services = [
        {'name': 'Home Cleaning', 'image': 'home_cleaning.png', 'description': 'Professional cleaning at your convenience.'},
        {'name': 'Plumbing', 'image': 'plumbing.png', 'description': 'Quick fixes and full installations by experts.'},
       
        {'name': 'Carpentry', 'image': 'carpentry.png', 'description': 'Expert woodwork for home improvements.'},
        {'name': 'Painting', 'image': 'painting.png', 'description': 'Freshen up your home with our expert painters.'},
        {'name': 'Electrician', 'image': 'electrician.png', 'description': 'Professional electrical services for all needs.'},
       
        {'name': 'AC Repair', 'image': 'ac_repair.png', 'description': 'Expert AC repairs to keep you cool all year round.'}
    ]
    
    return render(request, 'landing_page/service.html', {'services': services})

def service_detail(request, service_name):
    # Map from URL slug to real name
    service_map = {
        'home_cleaning': 'Home Cleaning',
        'plumbing': 'Plumbing',
        'carpentry': 'Carpentry',
        'painting': 'Painting',
        'electrician': 'Electrician',
        'ac_repair': 'AC Repair',
    }

    actual_service_name = service_map.get(service_name.lower())
    if not actual_service_name:
        raise Http404("Service not found")

    service = Service.objects.filter(name=actual_service_name).first()
    if not service:
        raise Http404("Service not found in DB")

    #  Load subservices associated with this service
    subservices = SubService.objects.filter(service=service)

    #  Load available workers for this service
    workers = WorkerProfile.objects.filter(service=service, user__is_available=True)

    return render(request, 'landing_page/service_detail.html', {
        'service': service,
        'subservices': subservices,
        'workers': workers,
    })



@login_required
def customer_profile(request):
    return render(request, template_name='customer_dashboard/customer_profile.html',context= {'user': request.user})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('log_profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'customer_dashboard/profile_form.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('login')
###########################################################################################################################
def worker_base(request):
    return render(request, template_name='worker_dashboard/log_base.html')

def worker_navbar(request):
    return render(request, template_name='worker_dashboard/log_nav.html')
@login_required
def worker_profile(request):
    return render(request, template_name='worker_dashboard/worker_profile.html',context= {'user': request.user})


@login_required
def worker_profile_update(request):
    if request.method == 'POST':
        form = WorkerProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('worker_profile')
    else:
        form = WorkerProfileUpdateForm(instance=request.user)  # Ei line change korun

    return render(request, 'worker_dashboard/worker_profile_update.html', {'form': form})


def logout(request):
    logout(request)
    return redirect('login')

def service_list(request):
    services = Service.objects.all()
    return render(request, 'landing_page/service.html', {'services': services})

def service_detail(request, service_name):
    print(f"DEBUG: service_detail called with: '{service_name}'")
    
    service_map = {
        'home_cleaning': 'Home Cleaning',
        'plumbing': 'Plumbing', 
        'carpentry': 'Carpentry',
        'painting': 'Painting',
        'electrician': 'Electrician',
        'ac_repair': 'AC Repair',
    }

    actual_service_name = service_map.get(service_name, service_name)

    service = Service.objects.filter(name=actual_service_name).first()
    if not service:
        from django.http import Http404
        raise Http404(f"Service '{service_name}' not found.")

    subservices = SubService.objects.filter(service=service)
    workers = User.objects.filter(user_type='worker', skills=service, is_available=True)

    context = {
        'service': service,
        'subservices': subservices,
        'workers': workers,
    }
    return render(request, 'landing_page/service_detail.html', context)


@login_required
def book_service(request, subservice_id):
    subservice = get_object_or_404(SubService, sub_id=subservice_id)

    if request.method == 'POST':
        scheduled_date = request.POST.get('scheduled_date')
        address = request.POST.get('address') or request.user.address
        worker_id = request.POST.get('worker_id')

        booking = Booking.objects.create(
            customer=request.user,
            service=subservice.service,
            subservice=subservice,
            scheduled_date=scheduled_date,
            address=address,
            worker=User.objects.get(user_id=worker_id) if worker_id else None
        )

        return redirect('booking_confirmation', booking_id=booking.bk_id)

    # If GET fallback
    return redirect('service_detail', service_name=subservice.service.name.lower().replace(" ", "_"))


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, bk_id=booking_id)

    # Assuming price is stored in the subservice model related to booking
    amount = booking.subservice.price if booking.subservice else 0

    context = {
        'booking': booking,
        'amount': amount,
    }
    return render(request, 'booking_confirmation.html', context)
