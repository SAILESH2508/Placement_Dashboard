from django.shortcuts import render

# Create your views here.
def placement_list(request):
    return render(request, 'placements/placement_list.html')

def placement_detail(request, pk):
    return render(request, 'placements/placement_detail.html', {'pk': pk})
