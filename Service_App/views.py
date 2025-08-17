from django.shortcuts import render

# Home page
def home(request):
    return render(request, 'landing_page/home.html')

# Login page
def login(request):
    return render(request, 'landing_page/login.html')

# Signup page
def signup(request):
    return render(request, 'landing_page/signup.html')

# About page
def about(request):
    return render(request, 'landing_page/about.html')

# FAQ page
def faq(request):
    return render(request, 'landing_page/faq.html')

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

# If you still want individual service pages (for detailed service info), you can create one dynamic detail page.
def service_detail(request, name):
    # Dictionary of all services
    services = {
        'home_cleaning': {'name': 'Home Cleaning', 'image': 'home_cleaning.png', 'description': 'Professional cleaning at your convenience.'},
        'plumbing': {'name': 'Plumbing', 'image': 'plumbing.png', 'description': 'Quick fixes and full installations by experts.'},
        'carpentry': {'name': 'Carpentry', 'image': 'carpentry.png', 'description': 'Expert woodwork for home improvements.'},
        'painting': {'name': 'Painting', 'image': 'painting.png', 'description': 'Freshen up your home with our expert painters.'},
        'electrician': {'name': 'Electrician', 'image': 'electrician.png', 'description': 'Professional electrical services for all needs.'},
        'ac_repair': {'name': 'AC Repair', 'image': 'ac_repair.png', 'description': 'Expert AC repairs to keep you cool all year round.'},
    }

    # Get the service data based on the name
    service_data = services.get(name)

    if service_data:
        return render(request, 'landing_page/service_detail.html', {'service': service_data})
    else:
        return render(request, 'landing_page/404.html')  # Return a 404 page if the service is not found