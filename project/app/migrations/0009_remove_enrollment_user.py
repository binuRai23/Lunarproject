# Generated by Django 5.1.1 on 2024-09-14 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_rename_contact_number_enrollment_contactnumber_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollment',
            name='user',
        ),
    ]
