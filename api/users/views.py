import smtplib
from email.mime.text import MIMEText

from django.conf import settings

from rest_framework import status, exceptions, viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import get_object_or_404

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

import rest_framework_simplejwt.exceptions
from rest_framework_simplejwt.tokens import RefreshToken

from api.books.models import Book
from api.books.serializers import BookViewSerializer
from api.users import serializers
from api.users.models import User
from api.users.serializers import UserSerializer, EmailSerializer, PasswordSerializer


def send_verification_email(email, message):
    sender = settings.EMAIL_HOST_USER
    subject = "Email Verification"

    msg = MIMEText(message, _charset='utf-8')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = email

    try:
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as smtp_server:
            smtp_server.login(sender, settings.EMAIL_HOST_PASSWORD)
            smtp_server.sendmail(sender, email, msg.as_string())
        return "Message sent successfully!"
    except smtplib.SMTPException as e:
        raise e


@api_view(['POST'])
def register(request: Request):
    try:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            data = {
                'refresh': str(refresh),
                'access': str(access_token),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def logout(request: Request):
    try:
        refresh = request.data.get('refresh')
        try:
            print(refresh)
            token = RefreshToken(token=refresh)

        except rest_framework_simplejwt.exceptions.TokenError as e:
            print(e)
            return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)
        token.blacklist()
        return Response({"status": "Logged out"}, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_verification_url(request):
    try:
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.data.get('email'))
        action_type = serializer.validated_data.get('action')
        url = f'http://127.0.0.1:8000/api/users/verify/email/?_id={user.id}&action={action_type}'
        send_verification_email(user.email, message=url)
        return Response(data={"detail": "Check email"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response("User with this email does not exists")
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    try:
        user_id = request.query_params.get('_id')
        action_type = request.query_params.get('action')
        if not user_id:
            raise exceptions.NotFound("No user id provided")
        user = User.objects.get(id=user_id)
        if not user:
            raise exceptions.NotFound("User does not exist")
        user.verified = True
        user.save()
        if action_type == 'reset':
            request.session['user'] = str(user.id)
            return Response(data={"detail": "http://127.0.0.1:8000/api/users/reset-password/"})
        elif action_type == 'verify':
            return Response(data={"detail": "http://127.0.0.1:8000/api/"})
        return Response(status=status.HTTP_200_OK)
    except exceptions.NotFound as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def reset_password(request):
    try:
        user_id = request.session.get('user')
        print(user_id)
        if not user_id:
            raise exceptions.NotFound("No session found")
        user = User.objects.get(id=user_id)
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response("Password reset successful", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except exceptions.NotFound as e:
        return Response(str(e), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(e)
        return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserViewSet(viewsets.ViewSet):
    serializer_class = serializers.UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data)

    def update(self, request):
        serializer = self.serializer_class(request.user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def destroy(self, request):
        request.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetUserBooksView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookViewSerializer

    def list(self, request, *args, **kwargs):
        user = get_object_or_404(User, email=kwargs['email'])
        books = Book.objects.filter(user=user, is_private=False).all()
        serializer = BookViewSerializer(books, many=True)
        return Response(serializer.data)


class GetUserProfileView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'email'
