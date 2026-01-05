from django.urls import path
from . import views

app_name = 'placements'

urlpatterns = [
    path('', views.placement_list, name='status'),
    path('<int:pk>/', views.placement_detail, name='detail'),
]
