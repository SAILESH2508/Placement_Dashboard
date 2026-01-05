from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),      # Removed legacy auth
    path('students/', include('students.urls')),
    path('companies/', include('companies.urls')),
    path('placements/', include('placements.urls')),
    # path('', include('dashboard.urls')),              # Removed legacy dashboard
    path('notifications/', include('notifications.urls')),
    path('analytics/', include('analytics.urls')),
    path('api/', include('rest_framework.urls')),
    path('api/auth/', include('accounts.api_urls')),
    
    # New API Endpoints
    path('api/dashboard/', include('dashboard.api_urls')),
    path('api/statistics/', include('analytics.api_urls')),
    path('api/companies/', include('companies.api_urls')),
    path('api/students/', include('students.api_urls')),
    path('api/placements/', include('placements.api_urls')),
    path('api/ml/', include('analytics.api_urls')),
    path('api/notifications/', include('notifications.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
