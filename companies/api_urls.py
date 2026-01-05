from django.urls import path
from .api_views import TopCompaniesView, CompanyListView

urlpatterns = [
    path('top/', TopCompaniesView.as_view(), name='company_top'),
    path('', CompanyListView.as_view(), name='company_list'),
]
