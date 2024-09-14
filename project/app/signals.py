from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Enrollment
from django.utils.crypto import get_random_string


@receiver(post_save, sender=Enrollment)
def send_enrollment_email(sender, instance, created, **kwargs):
    # """
    # Sends an email to the user with their login credentials after enrollment is created.
    # """
    if created:
        user = instance.user  # Get the user associated with the enrollment
        if not user.username:  # Check if user doesn't have a username yet
            # Create a random username and password
            random_password = get_random_string(8)

            # Set a username (email) and password for the user
            user.username = instance.email  # Assuming email is used as username
            user.set_password(random_password)
            user.save()

            # Send email with login credentials
            send_mail(
                'Your Login Information',
                f'Hello {instance.fullname},\n\n'
                f'You have been enrolled in {instance.course.name}.\n'
                f'Your login credentials are:\n'
                f'Username: {user.username}\nPassword: {random_password}\n\n'
                'Please log in to your account to start the course.',
                'noreply@yourwebsite.com',
                [instance.email],  # Send to the email the user provided
                fail_silently=False,
            )
            print("Email sent with login credentials.")  # Debugging
