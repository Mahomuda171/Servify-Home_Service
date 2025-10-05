from django.contrib import admin
from .models import *
from .models import Service, SubService


# Register your models here.
admin.site.register([User,Service, Booking, Review,Payment,Blog])
admin.site.register(SubService)
