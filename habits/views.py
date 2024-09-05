from datetime import time

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from habits.models import Habits
from habits.paginators import CustomPagination
from habits.permissions import IsOwner
from habits.serializers import HabitSerializer

from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Контроллер главной страницы сайта
    """
    template_name = 'habits/index.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        habits = Habits.objects.all()
        context_data['all_habits'] = habits.count()
        return context_data


class HabitsCreateAPIView(generics.CreateAPIView):
    """Создание привычки для авторизованного пользователя
    """

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """
        Переопределение метода create
        """
        habit = serializer.save()
        habit.owner = self.request.user

        # habit.utc_time = habit.time
        owner_time_offset = self.request.user.time_offset
        hour = habit.time.hour - owner_time_offset
        if hour > 24:
            hour -= 24
            habit.weekday_offset = -1
        elif hour < 0:
            hour = 24 + hour
            habit.weekday_offset = 1
        habit.utc_time = time(hour, int(habit.time.minute), 0, 0)

        habit.save()


class HabitsListAPIView(generics.ListAPIView):
    """Отображение привычек авторизованого пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class HabitsRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр выбранной привычки пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitsUpdateAPIView(generics.UpdateAPIView):
    """Обновление выбранной привычки пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)

    def perform_update(self, serializer):
        habit = serializer.save()
        owner_time_offset = self.request.user.time_offset
        hour = habit.time.hour - owner_time_offset
        if hour > 24:
            hour -= 24
            habit.weekday_offset = -1
        elif hour < 0:
            hour = 24 + hour
            habit.weekday_offset = 1
        habit.utc_time = time(hour, int(habit.time.minute), 0, 0)

        habit.save()


class HabitsDestroyAPIView(generics.DestroyAPIView):
    """Удаление выбранной привычки пользователя"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class HabitsPublicListAPIView(generics.ListAPIView):
    """Список публичных привычек"""

    serializer_class = HabitSerializer
    queryset = Habits.objects.all()
    permission_classes = (AllowAny,)
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Habits.objects.filter(is_public=True)
        return queryset
