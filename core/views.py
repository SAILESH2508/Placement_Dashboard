# core/views.py
from django.shortcuts import redirect

def home(request):
    return redirect('dashboard')
