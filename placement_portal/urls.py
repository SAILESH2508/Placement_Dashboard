from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.auth_api import LoginView, RegisterView, MeView, ForgotPasswordView

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ AUTH (final, clean, no duplicates)
    path("api/auth/login/", LoginView.as_view(), name="login"),
    path("api/auth/register/", RegisterView.as_view(), name="register"),
    path("api/auth/me/", MeView.as_view(), name="me"),
    path("api/auth/forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # ✅ APP endpoints
    path("api/", include("core.urls")),

    # ✅ ML endpoints
    path("api/ml/", include("ml_model.urls")),
]
