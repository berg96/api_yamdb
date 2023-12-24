from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer, TokenSerializer
from .utils import send_verification_email, generate_verification_code

User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            code = generate_verification_code()
            try:
                user = User.objects.get(username=username)
                user.verification_code = code
                user.save()
            except User.DoesNotExist:
                User.objects.create(
                    username=username, email=email, verification_code=code
                )
            send_verification_email(email, code)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            code = serializer.validated_data['confirmation_code']
            user = User.objects.get(username=username)
            if user.verification_code != code:
                return Response(
                    'Неверный код доступа', status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            data = {
                'token': str(refresh.access_token)
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
