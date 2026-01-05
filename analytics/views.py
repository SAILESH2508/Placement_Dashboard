from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def stats(request):
    return render(request, 'analytics/stats.html')
