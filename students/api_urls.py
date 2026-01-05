from django.urls import path
from .api_views import StudentListView

urlpatterns = [
    path('', StudentListView.as_view(), name='student_list_api'),
]
