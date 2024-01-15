import random
import os

from dotenv import load_dotenv
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (DestroyAPIView, ListCreateAPIView,
                                     RetrieveUpdateAPIView, get_object_or_404)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .permissions import (IsAdminUserOrReadOnly,
                          IsAuthorAdminModeratorOrReadOnlyPermission,
                          IsAdminRole)
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TokenSerializer, UserSerializer,
                          UserSerializerForAdmin, TitleReadSerializer,
                          TitleWriteSerializer)
from reviews.models import Category, Genre, Review, Title, RANGE_CODE

load_dotenv()

User = get_user_model()
SENDER_EMAIL = os.getenv('SENDER_EMAIL')


class SignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = SignupSerializer(request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        code = str(random.randint(*RANGE_CODE))
        user, _ = User.objects.get_or_create(username=username, email=email)
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {code}',
            SENDER_EMAIL,
            [email],
            fail_silently=False,
        )
        return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    user, _ = User.objects.get_or_create(email=email, username=username)

    # generate token
    # confirmation_code = default_token_generator.make_token(user)
    confirmation_code = str(random.randint(*RANGE_CODE))
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        SENDER_EMAIL,
        [email],
        fail_silently=False,
    )
    user.confirmation_code = confirmation_code
    return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = [AllowAny]
    serializer_class = TokenSerializer

    def post(self, request):
        user = get_object_or_404(
            User, username=request.data.get('username')
        )
        if (user.confirmation_code != request.data.get(
            'confirmation_code'
        )):
            user.confirmation_code = None
            return Response(
                'Неверный код доступа', status=status.HTTP_400_BAD_REQUEST
            )
        refresh = RefreshToken.for_user(user)
        data = {
            'token': str(refresh.access_token)
        }
        return Response(data)


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerForAdmin
    permission_classes = [IsAdminRole]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserDetailForAdmin(UserDetail, DestroyAPIView):
    permission_classes = [IsAdminRole]
    serializer_class = UserSerializerForAdmin
    http_method_names = ['get', 'patch', 'delete']

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class CategoryViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']


class GenreViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
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
    permission_classes = [IsAuthorAdminModeratorOrReadOnlyPermission]
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
