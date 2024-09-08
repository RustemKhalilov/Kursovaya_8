from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsUserOwner, IsSuperuserOrStaff
from users.serializers import UserSerializer, UserLimitedSerializer
from users.forms import UserRegisterForm, UserProfileForm


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """Отображение либо редактирование информации об авторизованном пользователе"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOwner, IsAuthenticated)


class UserListAPIView(ListAPIView):
    """Список пользователей"""

    form_class = UserRegisterForm
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.permission_classes == (IsSuperuserOrStaff,):
            return UserSerializer
        return UserLimitedSerializer


class UserCreateAPIView(CreateAPIView):
    """Создание пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
