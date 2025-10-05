from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Service_App import views  # Import only once

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('faq/', views.faq, name='faq'),
    path('service/', views.service, name='service'),  # Services listing page
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    
    # ✅ FIXED: Only ONE service_detail URL pattern
    path('service/<str:service_name>/', views.service_detail, name='service_detail'),
    
    path('blog/', views.blog, name='blog'),
    path('create_blog/', views.create_blog, name='create_blog'),
    path('admin/blog/response/<uuid:blog_id>/', views.admin_response, name='admin_blog_response'),

   #path('log_base/', views.log_base, name='log_base'),
    #path('log_nav/', views.log_nav, name='log_nav'),
    path('customer_profile/', views.customer_profile, name='customer_profile'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('update_profile/', views.update_profile, name='update_profile'),

    path('worker_base/', views.worker_base, name='worker_base'),
    path('worker_navbar/', views.worker_navbar, name='worker_navbar'),
    path('worker_profile/', views.worker_profile, name='worker_profile'),
    path('logout/', views.logout, name='logout'),
    path('worker_profile_update/', views.worker_profile_update, name='worker_profile_update'),
    
    # ✅ Keep these additional service URLs
    path('services/', views.service_list, name='service_list'),
    path('book/<uuid:subservice_id>/', views.book_service, name='book_service'),
    path('booking-confirmation/<uuid:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)