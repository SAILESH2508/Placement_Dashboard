from django.shortcuts import render

# Create your views here.
def notification_list(request):
    return render(request, 'notifications/notification_list.html')

def notification_detail(request, pk):
    return render(request, 'notifications/notification_detail.html', {'pk': pk})
