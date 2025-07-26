from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer
from .tasks import send_welcome_email
from django.contrib.auth import login
from .serializers import LoginSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # trigger asynchronous welcome email
        send_welcome_email.delay(user.username, user.email)

        headers = self.get_success_headers(serializer.data)
        return Response({"detail": "Registration successful"}, status=status.HTTP_201_CREATED, headers=headers)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return Response({"detail": "Login successful"}) 