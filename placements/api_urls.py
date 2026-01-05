from django.urls import path
from .api_views import PlacementListView

urlpatterns = [
    path('', PlacementListView.as_view(), name='placement_list_api'),
]
