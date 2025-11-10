import logging
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import *
from django.utils import timezone  # Add this import at the top

# Configure logger
logger = logging.getLogger('backend')

# Helper to generate access and refresh tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info("Register attempt: email=%s", request.data.get("email"))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        logger.info("User registered successfully: id=%s, email=%s", user.id, user.email)
        return Response({
            "user": UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)



class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        logger.info("Login attempt: email=%s", email)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = get_tokens_for_user(user)

        # ✅ Update last login timestamp
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        logger.info("User logged in successfully: id=%s, email=%s, last_login=%s", user.id, user.email, user.last_login)
        return Response({
            "user": UserSerializer(user).data,
            "token": token
        }, status=status.HTTP_200_OK)



class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        logger.info("Token refresh attempt")
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            logger.info("Token refreshed successfully")
        except Exception as e:
            logger.error("Token refresh failed: %s", str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'access': serializer.validated_data['access'],
            'refresh': serializer.validated_data.get('refresh', request.data.get('refresh'))
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        logger.info("Logout attempt: user_id=%s", user.id)
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("Logout successful: user_id=%s", user.id)
            return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Logout failed for user_id=%s: %s", user.id, str(e))
            return Response({"error": "Invalid token or already blacklisted"}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        serializer.send_reset_email(email)
        return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token = kwargs.get('token')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data["password"]
        serializer.reset_password(uid, token, password)
        return Response( "Password reset successfully", status=status.HTTP_200_OK)
        

class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logger.info("Health check requested")
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response("Password changed successfully.", status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)