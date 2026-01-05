from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path('', include('students.urls')),  # we'll put dashboard and student urls here
    path('companies/', include('companies.urls')),
    path('placements/', include('placements.urls')),
    path('notifications/', include('notifications.urls')),
    # Removed conflicting home path
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



from rest_framework import routers
from students.api import StudentViewSet
router = routers.DefaultRouter()
router.register(r'api/students', StudentViewSet)
urlpatterns += router.urls
