from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Product
from .forms import PaymentForm  # Assuming you have a form for handling payments
import uuid
from uuid import uuid4
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
import json
import requests
from django.shortcuts import render, get_object_or_404
from .models import Product  # Assuming you have a Product model
from django.views.decorators.csrf import csrf_exempt
from requests.exceptions import Timeout, RequestException
from django.core.mail import send_mail
from .forms import EnrollmentForm
from django.conf import settings
from .signals import send_enrollment_email
from django.contrib.auth import authenticate, login
from django.contrib import messages

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html',{'product': product})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'course_list.html', {'courses': courses})

from django.shortcuts import render
from .models import Course

def home(request):
    courses = Course.objects.all()
    products = Product.objects.all()
    # Combine both courses and products in a single context dictionary
    context = {
        'courses': courses,
        'products': products
    }
    return render(request, 'home.html', context)

from .forms import LoginForm

def Login(request):
  if request.method == 'POST':
        # Get email and password from the form data
        email = request.POST.get('username')
        password = request.POST.get('password')

        # Try to authenticate the user using the provided credentials
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in if authentication is successful
            login(request, user)
            return redirect('dashboard')  # Redirect to the user dashboard
        else:
            # Display an error message if authentication fails
            messages.error(request, 'Invalid email or password')

    # If it's a GET request or authentication fails, render the login page again
  return render(request, 'login.html')

def enrollment_form(request):
    courses = Course.objects.all()

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            # Generate random username and password
            generated_username = form.cleaned_data['email']  # Using email as username
            generated_password = get_random_string(8)  # Generates a random 8-character password
           

            # Create user
            user = User.objects.create_user(
                username=generated_username,
                password=generated_password,
                email=form.cleaned_data['email'],
            )
           
            
            enrollment = form.save(commit=False)
            enrollment.user = user  # Link the user to the enrollment
            enrollment.course = form.cleaned_data['course']  # Link the selected course
            enrollment.save()  # Save the enrollment data
            print("Enrollment saved successfully.")  # Debugging
            
            # Send email with login info
            subject = 'Your Enrollment Details and Login Information'
            message = f"Dear {form.cleaned_data['fullname']},\n\n" \
                      f"You have successfully enrolled in {form.cleaned_data['course']}. Here are your login details:\n" \
                      f"Username: {generated_username}\n" \
                      f"Password: {generated_password}\n\n" \
                      f"Please log in using these credentials."
            recipient_list = [form.cleaned_data['email']]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            return redirect('home')  # Redirect to user dashboard or another page
        else:
            print("Form errors:", form.errors)  # Debugging
    else:
        form = EnrollmentForm()

    return render(request, 'enrollment_form.html', {'form': form, 'courses': courses})

def paymentform(request):
    products = Product.objects.all()
    uid = uuid.uuid4()
    
    context = {
        'uid': uid,
        'products': products,
    }
    return render(request, 'payment.html',context)

@csrf_exempt 
def initkhalti(request):
    
    url = "https://a.khalti.com/api/v2/epayment/initiate/"
    
        # print("Received POST Data:", request.POST)
    return_url = request.POST.get('return_url')
    purchase_order_id = request.POST.get('purchase_order_id')
    amount= request.POST.get('Amount')
    name = request.POST.get('fullname')
    email = request.POST.get('email')
    phone = request.POST.get('contact')

    # try:
    #     amount_in_paisa = int(float(amount) * 100)  # Convert rupees to paisa
    #     print(f"Amount in paisa: {amount_in_paisa}")  # Debugging: Check the converted amount
    # except (TypeError, ValueError) as e:
    #     print(f"Invalid amount: {e}")
    #     return HttpResponseBadRequest('Invalid amount provided.')

    print('return_url', return_url)
    print('purchase_order_id', purchase_order_id)
    print('amount',amount)
    
    payload = json.dumps({
        "return_url": return_url,
        "website_url": "http://127.0.0.1:8000",
        "amount":  amount,
        "purchase_order_id": purchase_order_id,
        "purchase_order_name": "test",
        "customer_info": {
        "name": name ,
        "email": email,
        "phone": phone,
        }
    })
    headers = {
        'Authorization': 'key a7c272e66528458f98063c8e80ed22fd',
        'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    newres = json.loads(response.text)
    print(newres)
    return redirect(newres['payment_url'])
    pass
        

@login_required
def dashboard(request):
    user = request.user  # Get the currently logged-in user
    enrollments = Enrollment.objects.filter(user=user)  # Assuming user foreign key

    return render(request, 'dashboard.html', {
        'user': user,
        'enrollments': enrollments,
    })

    
def verifyKhalti(request):
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    pidx = request.GET.get('pidx')
    headers = {
        'Authorization': 'key a7c272e66528458f98063c8e80ed22fd',
        'Content-Type': 'application/json',
    }
    payload = json.dumps({
        'pidx': pidx
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    newres = json.loads(response.text)
    print(newres)
    if new_res['status'] == 'Completed':
            
            #Updating the values in the database of course payment
            payment = get_object_or_404(CoursePayment,pidx=pidx)  
            
            payment.status = 'COMPLETED'
            payment.payment_method = 'KHALTI'
            payment.save()
            
            
            user = payment.user    #user refers to the name inside the CoursePayment
            course = payment.course
            
            user.is_Student = True
            user.save()
            
            course.course_purchased = True
            course.save()
            print(f"Payment completed by {user.f_name} for course {course.name}")
            return render(request, 'dashboard.html', {'user': user, 'course': course})
            
            
            # i want to fetch the user and course for the payment applied
            
    return render(request, 'payment_success.html')
    