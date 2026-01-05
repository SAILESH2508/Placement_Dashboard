from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'is_active', 'posted_at')
    search_fields = ('title', 'company__name', 'location')
    list_filter = ('company', 'is_active')
    date_hierarchy = 'posted_at'

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'job', 'status', 'applied_at')
    search_fields = ('student__user__username', 'job__title', 'status')
    list_filter = ('status', 'job__company')
    date_hierarchy = 'applied_at'
