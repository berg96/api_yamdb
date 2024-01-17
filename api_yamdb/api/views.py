import os
import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import (IsAdminRole, IsAdminUserOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnlyPermission)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          TokenSerializer, UserSerializer)
from reviews.models import RANGE_CODE, Category, Genre, Review, Title

User = get_user_model()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    try:
        user, _ = User.objects.get_or_create(email=email, username=username)
    except IntegrityError as error:
        error_response = {}
        if 'username' in str(error):
            error_response['username'] = [
                username, 'Используется другим пользователем'
            ]
        if 'email' in str(error):
            if User.objects.filter(username=username).exists():
                error_response['username'] = [
                    username, 'Используется другим пользователем'
                ]
            error_response['email'] = [
                email, 'Используется другим пользователем'
            ]
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = str(random.randint(*RANGE_CODE))
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        SENDER_EMAIL,
        [email],
        fail_silently=False,
    )
    user.confirmation_code = confirmation_code
    user.save()
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def give_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if (user.confirmation_code != serializer.validated_data[
            'confirmation_code'
    ]):
        user.confirmation_code = None
        user.save()
        return Response(
            {'detail': 'Неверный код доступа'},
            status=status.HTTP_400_BAD_REQUEST
        )
    refresh = RefreshToken.for_user(user)
    data = {
        'token': str(refresh.access_token)
    }
    return Response(data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class ModelViewSetWithCommonFunctionality(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']


class CategoryViewSet(ModelViewSetWithCommonFunctionality):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ModelViewSetWithCommonFunctionality):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorAdminModeratorOrReadOnlyPermission]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title()
        )


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorAdminModeratorOrReadOnlyPermission]
    serializer_class = CommentsSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )
