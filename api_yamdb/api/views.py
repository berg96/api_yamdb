import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import (
    IsAdmin, IsAdminOrReadOnly, IsAuthorAdminModeratorOrReadOnly
)
from .serializers import (
    CategorySerializer, CommentsSerializer, GenreSerializer, ReviewSerializer,
    SignupSerializer, TitleReadSerializer, TitleWriteSerializer,
    TokenSerializer, UserSerializer, UserSerializerForAdmin
)
from reviews.models import Category, Genre, Review, Title

User = get_user_model()

ERROR_IN_USE = 'Используется другим пользователем'


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    try:
        user, _ = User.objects.get_or_create(email=email, username=username)
    except IntegrityError:
        result = {}
        if User.objects.filter(username=username).exists():
            result['username'] = [username, ERROR_IN_USE]
            if User.objects.filter(email=email).exists():
                result['email'] = [email, ERROR_IN_USE]
        else:
            result['email'] = [email, ERROR_IN_USE]
        raise ValidationError(result)
    confirmation_code = ''.join(
        random.choice(settings.CODE_CHARACTERS)
        for _ in range(settings.MAX_LENGTH_CODE)
    )
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
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
    confirmation_code = serializer.validated_data['confirmation_code']
    if (
        user.confirmation_code != confirmation_code
        or confirmation_code == settings.INVALID_CODE
    ):
        user.confirmation_code = settings.INVALID_CODE
        user.save()
        raise ValidationError({'confirmation_code': ['Неверный код доступа']})
    refresh = RefreshToken.for_user(user)
    data = {
        'token': str(refresh.access_token)
    }
    return Response(data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializerForAdmin
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        url_path=settings.SELF_PROFILE_NAME
    )
    def profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClassificationViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(ClassificationViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ClassificationViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('name')
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAuthorAdminModeratorOrReadOnly]
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
    permission_classes = [IsAuthorAdminModeratorOrReadOnly]
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
