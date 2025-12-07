from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
import logging

logger = logging.getLogger(__name__)


# ✅ Helper: create tokens
def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }


# ✅ LOGIN
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and password are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = authenticate(username=username, password=password)
            if user is None:
                logger.warning(f"Failed login attempt for username: {username}")
                return Response(
                    {"error": "Invalid username or password"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )

            if not user.is_active:
                return Response(
                    {"error": "Account is disabled"}, 
                    status=status.HTTP_403_FORBIDDEN
                )

            tokens = generate_tokens(user)
            logger.info(f"User {username} logged in successfully")

            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "tokens": tokens
            })
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return Response(
                {"error": "An error occurred during login"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

# ✅ AUTH ME
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })


# ✅ REGISTER
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        # Validation
        if not username or not email or not password:
            return Response(
                {"error": "Username, email, and password are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(password) < 8:
            return Response(
                {"error": "Password must be at least 8 characters long"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except DjangoValidationError:
            return Response(
                {"error": "Invalid email format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already registered"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            logger.info(f"New user registered: {username}")
            
            tokens = generate_tokens(user)
            
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                },
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            return Response(
                {"error": "Failed to create user"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ✅ FORGOT PASSWORD
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        
        if not email:
            return Response(
                {"error": "Email is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_email(email)
        except DjangoValidationError:
            return Response(
                {"error": "Invalid email format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user exists (but don't reveal this for security)
        try:
            user = User.objects.filter(email=email).first()
            if user:
                # TODO: Implement actual password reset email
                # For now, just log it
                logger.info(f"Password reset requested for: {email}")
                # In production, send email with reset token
                
            # Always return success to prevent email enumeration
            return Response({
                "message": "If an account exists with this email, password reset instructions have been sent"
            })
        except Exception as e:
            logger.error(f"Password reset error: {str(e)}")
            return Response(
                {"error": "An error occurred"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
