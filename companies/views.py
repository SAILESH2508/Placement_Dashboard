from django.shortcuts import render

# Create your views here.

def company_list(request):
    return render(request, 'companies/company_list.html')

def company_detail(request, pk):
    return render(request, 'companies/company_detail.html', {'pk': pk})
