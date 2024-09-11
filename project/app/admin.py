from django.contrib import admin
from .models import Course
from .models import Product

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description', 'image')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'created_at', 'image', 'price')