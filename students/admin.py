from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'course', 'year', 'cgpa')
    search_fields = ('user__username', 'user__first_name', 'roll_no', 'course')
