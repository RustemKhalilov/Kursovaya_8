from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (
    HabitsListAPIView,
    HabitsRetrieveAPIView,
    HabitsCreateAPIView,
    HabitsUpdateAPIView,
    HabitsDestroyAPIView,
    HabitsPublicListAPIView,
    HomeView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("list/", HabitsListAPIView.as_view(), name="habits_list"),
    path("<int:pk>/", HabitsRetrieveAPIView.as_view(), name="habits_retrieve"),
    path("create/", HabitsCreateAPIView.as_view(), name="habits_create"),
    path("<int:pk>/update/", HabitsUpdateAPIView.as_view(), name="habits_update"),
    path(
        "<int:pk>/delete/",
        HabitsDestroyAPIView.as_view(),
        name="habits_delete",
    ),
    path("public/", HabitsPublicListAPIView.as_view(), name="public_list"),
]
