from django.contrib import admin
from django.urls import path
from Service_App import views  # Make sure to import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('service/', views.service, name='service'),  # The page displaying all services
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('service/<str:name>/', views.service_detail, name='service_detail'),  # Detail page for each service
    #path('faq/', views.faq, name='faq'),
    # Add the contact page URL here
    #path('contact/', views.contact, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
