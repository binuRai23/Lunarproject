from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Payment, Product
from .forms import PaymentForm  # Assuming you have a form for handling payments
import uuid

from django.shortcuts import render, get_object_or_404
from .models import Product  # Assuming you have a Product model

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


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


def enrollment_form(request):
    courses = Course.objects.all()
    return render(request, 'enrollment_form.html', {'courses': courses})

@login_required
def payment(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.course = enrollment.course
            payment.save()
            enrollment.payment_status = 'Completed'
            enrollment.save()

            # Redirect to the user's dashboard after successful payment
            return redirect('dashboard')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'enrollment': enrollment})


@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'enrollments': enrollments})
