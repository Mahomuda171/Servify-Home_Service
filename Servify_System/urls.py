from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from Service_App import views as home
from Service_App import views as worker
from Service_App import views as login_user

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

    path('log_base/', login_user.log_base, name='log_base'),
    path('log_nav/', login_user.log_nav, name='log_nav'),
    path('customer_profile/', login_user.customer_profile, name='customer_profile'),
    path('logout/', login_user.logout_view, name='logout'),
    path('update_profile/', login_user.update_profile, name='update_profile'),


    path('worker_profile/', worker.worker_profile, name='worker_profile'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
