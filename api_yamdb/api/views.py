import re

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView, \
    DestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, filters, permissions


from .serializers import (
    SignupSerializer, TokenSerializer, UserSerializer,
    CategorySerializer, GenreSerializer, TitleReadSerializer,
    TitleWriteSerializer, ReviewSerializer, CommentsSerializer
)
from .utils import send_verification_email, generate_verification_code
from reviews.models import Category, Genre, Title, Review
from .permissions import (IsAdminUserOrReadOnly,
                          IsAuthorAdminSuperuserOrReadOnlyPermission, )

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
            user = get_object_or_404(User, username=username)
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


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def perform_create(self, serializer):
        username = serializer.validated_data.get('username')
        if not re.fullmatch(r'^[\w.@+-]+\Z', username):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if serializer.validated_data.get('role') == 'admin':
            serializer.save(is_staff=True)
        super().perform_create(serializer)


class UserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        print(self.request.user.username)
        return self.request.user


class UserDetailForAdmin(UserDetail, DestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_object(self):
        print(self.request.user.username)
        print(self.kwargs)
        return get_object_or_404(User, username=self.kwargs['username'])

    def perform_update(self, serializer):
        if serializer.validated_data['role'] == 'admin':
            serializer.save(is_staff=True)
        if (serializer.validated_data['role'] == 'moderator' or
                serializer.validated_data['role'] == 'user'):
            serializer.save(is_staff=False)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
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
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_fields = ('category__slug', 'genre__slug', 'name', 'year')

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
