from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Service_App import views as home
from Service_App import views as customer
from Service_App import views as worker


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.home, name='home'),
    path('about/', home.about, name='about'),
    path('faq/', home.faq, name='faq'),
    path('service/', home.service, name='service'),  # The page displaying all services
    path('login/', home.login, name='login'),
    path('signup/', home.signup, name='signup'),
    path('service/<str:name>/', home.service_detail, name='service_detail'),  # Detail page for each service
    path('blog/', home.blog, name='blog'),
    path('create_blog/', home.create_blog, name='create_blog'),
    path('admin/blog/response/<uuid:blog_id>/', home.admin_response, name='admin_blog_response'),
    path('customer/', customer.customer, name='customer'),
    path('worker/', worker.worker, name='worker'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
