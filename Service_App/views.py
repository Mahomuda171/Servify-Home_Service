from django.shortcuts import render

def home(request):
    return render(request, template_name='landing_page/home.html')
def login(request):
    return render(request, template_name='landing_page/login.html')
def signup(request):
    return render(request, template_name='landing_page/signup.html')
def about(request):
    return render(request, template_name='landing_page/about.html')
def faq(request):
    return render(request, template_name='landing_page/faq.html')
def service(request):
    return render(request, template_name='landing_page/service.html')

