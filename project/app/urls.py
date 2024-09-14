from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enroll/', views.enrollment_form, name='enroll'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('payment/', views.paymentform, name='payment'),
    path('login/', views.Login, name='login'),
    # khalti url 
    path('initiate', views.initkhalti, name='initiate'),
    path('verify', views.verifyKhalti, name= "verify"),
]
