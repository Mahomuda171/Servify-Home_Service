import uuid
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    USER_TYPE_CHOICES = (
        ('normal', 'User'),
        ('worker', 'Worker'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phn_Num = models.CharField(max_length=15, blank=True, null=True)

    # Worker-specific fields
    skills = models.ManyToManyField('Service', blank=True, related_name='workers')
    experience = models.PositiveIntegerField(default=0, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
   # price = models.DecimalField(max_digits=8, decimal_places=2)  # Changed from CharField
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    bk_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_made')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_assigned', blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings')
    subservice = models.ForeignKey('SubService', on_delete=models.CASCADE, null=True, blank=True, related_name='bookings')
    date_created = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField()  # When the service should be performed
    completed_date = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    address = models.TextField(blank=True, null=True)  # Service address if different from user address

    def __str__(self):
        return f"Booking #{self.bk_id} - {self.service.name}"


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    )

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review for {self.worker.username} by {self.user.username}"


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    )

    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Payment #{self.payment_id} - {self.amount}"

class Blog(models.Model):
    blog_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField(max_length=2000)
    requirements = models.TextField(max_length=1000, help_text="Describe your requirements in detail")
    contact_info = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_response = models.TextField(max_length=1000, blank=True)
    contacted = models.BooleanField(default=False)

    def __str__(self):
        return f"Blog by {self.user.username} - {self.title}"



# Add these to your existing models.py

class SubService(models.Model):
    sub_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='subservices')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=50, default="1-2 hours")
    is_popular = models.BooleanField(default=False)
    image = models.ImageField(upload_to='subservices/',null=True, blank=True)
    def __str__(self):
        return f"{self.service.name} - {self.name}"

class WorkerProfile(models.Model):
    worker = models.OneToOneField(User, on_delete=models.CASCADE, related_name='worker_profile')
    subservices = models.ManyToManyField(SubService, related_name='workers')
    experience = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.0)
    hourly_rate = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bio = models.TextField(blank=True, null=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    available_from = models.TimeField(default='09:00')
    available_to = models.TimeField(default='18:00')
    
    def __str__(self):
        return f"Worker Profile - {self.worker.username}"

# Update your existing Booking model to include subservice
# Add this field to your existing Booking model:
# subservice = models.ForeignKey(SubService, on_delete=models.CASCADE, null=True, blank=True)