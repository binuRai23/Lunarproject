
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='courseimage/')

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    # New fields for name, contact, and email
    fullname = models.CharField(max_length=100)
    contactnumber = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)  # New field for address

    # Course price (can be dynamically calculated from the selected course)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # New field for price
    
    completed = models.BooleanField(default=False)  # To track course completion
    certificate = models.ImageField(upload_to='certificates/', null=True, blank=True)  # Certificate upload field

    def __str__(self):
        return f'{self.full_name} ({self.email}) - {self.course.title} - {"Completed" if self.completed else "In Progress"}'

from django.db import models
from django.contrib.auth.models import User
from .models import Course  
from uuid import uuid4

class CoursePayment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('FAILED', 'FAILED'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CREDIT_CARD', 'CREDIT_CARD'),
        ('PAYPAL', 'PAYPAL'),
        ('ESEWA', 'ESEWA'),
        ('KHALTI', 'KHALTI'),
       
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING') 
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=200, unique=True, default=uuid4)
    pidx = models.CharField(max_length=255, unique=True)
    
    def __str__(self):
        return f'{self.user.f_name} - {self.course.name} - {self.amount} ({self.status})'


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

   