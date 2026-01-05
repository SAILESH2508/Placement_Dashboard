from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'city', 'contact_email', 'created_at')
    search_fields = ('name', 'city', 'contact_email')
    list_filter = ('city',)
