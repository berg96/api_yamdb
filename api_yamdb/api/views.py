import os
import random
import re

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from dotenv import load_dotenv
from rest_framework import filters, permissions, status, viewsets
from rest_framework.generics import (DestroyAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import (IsAdminUserOrReadOnly,
                          IsAuthorAdminSuperuserOrReadOnlyPermission)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer,
                          UserSerializerForAdmin)
from reviews.models import Category, Genre, Review, Title

load_dotenv()

SENDER_EMAIL = os.getenv('SENDER_EMAIL')
User = get_user_model()


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            if not re.fullmatch(r'^[\w.@+-]+\Z', username):
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            email = serializer.validated_data['email']
            code = str(random.randint(1000, 9999))
            try:
                user = User.objects.get(username=username)
                user.confirmation_code = code
                user.save()
            except User.DoesNotExist:
                User.objects.create(
                    username=username, email=email, confirmation_code=code
                )
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {code}',
                SENDER_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User, username=serializer.validated_data['username']
            )
            # if (user.confirmation_code != serializer.validated_data[
            #     'confirmation_code'
            # ]):
            #     return Response(
            #         'Неверный код доступа', status=status.HTTP_400_BAD_REQUEST
            #     )
            refresh = RefreshToken.for_user(user)
            data = {
                'token': str(refresh.access_token)
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerForAdmin
    permission_classes = [IsAdminUser]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailForAdmin(UserDetail, DestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializerForAdmin
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def perform_update(self, serializer):
        role = serializer.validated_data.get('role')
        if role == 'admin':
            serializer.save(is_staff=True)
        if role == 'moderator' or role == 'user':
            serializer.save(is_staff=False)
        super().perform_update(serializer)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    # serializer_class = TitleReadSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

    # def perform_create(self, serializer):
    #     print(serializer.validated_data)
    #     genres = serializer.validated_data['genre']
    #     category = serializer.validated_data['category']
    #     serializer.save(category=category)
    #     for genre in genres:
    #         serializer.instance.genre.add(genre)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthorAdminSuperuserOrReadOnlyPermission,
        permissions.IsAuthenticatedOrReadOnly
    ]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(
            Title, pk=self.kwargs.get('title_id')
        )
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(
            author=self.request.user, title=title
        )


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthorAdminSuperuserOrReadOnlyPermission,
        permissions.IsAuthenticatedOrReadOnly
    ]
    serializer_class = CommentsSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user, review=review
        )
