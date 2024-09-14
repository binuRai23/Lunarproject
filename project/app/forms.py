from django import forms
from .models import CoursePayment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = CoursePayment
        fields = ['amount', 'payment_method']
        widgets = {
            'amount': forms.HiddenInput(),  # Hide amount field, it should be filled automatically
        }

from .models import Enrollment

class EnrollmentForm(forms.ModelForm):
    # username = forms.CharField(max_length=150, required=True)
    # password = forms.CharField(widget=forms.PasswordInput, required=True)
    class Meta:
        model = Enrollment
        fields = ['fullname', 'contactnumber', 'email', 'course','address','price']  # The fields you want to capture

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)