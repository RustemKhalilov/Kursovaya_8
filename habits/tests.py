from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habits
from users.models import User


class HabitTestCase(APITestCase):
    """Тестирование модели Habits"""

    def setUp(self):
        """Создание тестовой модели Пользователя (с авторизацией) и Привычки"""

        self.user = User.objects.create(
            email="user2@list.ru",
            password="qwerty12345",
            tg_chat_id="616492316",
        )
        self.client.force_authenticate(user=self.user)

        self.habit = Habits.objects.create(
            owner=self.user,
            place="Ванная",
            time="06:45:00",
            action="Принять ванную",
            periodicity=1,
            duration=10,
        )

        self.habit_nice_false = Habits.objects.create(
            owner=self.user,
            place="Спальня",
            time="7:50:00",
            action="Сделать зарядку",
            is_nice=False,
            related=self.habit,
            periodicity=1,
            duration=10,
            is_public=False,
        )

    def test_create_habit(self):
        """Тестирование создания привычки"""

        url = reverse("habits:habits_create")
        data = {
            "owner": self.user.pk,
            "place": "Автомобиль",
            "time": "8:20:00",
            "action": "Осмотр автомобиля",
            "duration": 5,
            "periodicity": 1,
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
        }

        response = self.client.post(url, data=data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("owner"), self.user.pk)
        self.assertEqual(data.get("place"), "Автомобиль")
        self.assertEqual(data.get("time"), "08:20:00")
        self.assertEqual(data.get("action"), "Осмотр автомобиля")
        self.assertEqual(data.get("duration"), 5)
        self.assertEqual(data.get("periodicity"), 1)
        self.assertEqual(data.get("friday"), True)

    def test_create_habit_duration_periodicy_validator(self):
        """Тестирование работы валидаиора"""

        url = reverse("habits:habits_create")
        data = {
            "owner": self.user.pk,
            "place": "Спальня",
            "time": "8:20:00",
            "action": "Сделать зарядку",
            "duration": 10,
            "periodicity": 8,
        }

        response = self.client.post(url, data=data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_week_periodicity_validator(self):
        """Хотя бы один день в неделе должен быть выбран"""

        url = reverse("habits:habits_create")
        data = {
            "owner": self.user.pk,
            "place": "Автомобиль",
            "time": "8:20:00",
            "action": "Осмотр автомобиля",
            "duration": 5,
            "periodicity": 8,
            "sunday": False,
            "monday": False,
            "tuesday": False,
            "wednesday": False,
            "thursday": False,
            "friday": False,
            "saturday": False,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_logic_good_habits_1(self):
        """Тестирование работы валидатора логики создания привычек"""

        # У приятной привычки не может быть вознаграждения или связанной привычки.

        url = reverse("habits:habits_create")
        data = {
            "owner": self.user.pk,
            "place": "Автомобиль",
            "time": "8:20:00",
            "action": "Осмотр автомобиля",
            "is_nice": True,
            "duration": 5,
            "periodicity": 1,
            "prize": "Похвалить машину",
        }

        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_logic_good_habits_2(self):
        """Тестирование работы валидатора логики создания привычек"""

        # Исключить одновременный выбор связанной привычки и указания вознаграждения.

        url = reverse("habits:habits_create")
        data2 = {
            "owner": self.user.pk,
            "place": "Автомобиль",
            "time": "8:20:00",
            "action": "Осмотр автомобиля",
            "is_nice": False,
            "related": self.habit,
            "duration": 5,
            "periodicity": 1,
            "prize": "Похвалить машину еще раз",
        }
        response = self.client.post(url, data=data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_habit_logic_good_habits_3(self):
        """Тестирование работы валидатора логики создания привычек"""

        # В связанные привычки могут попадать только привычки с признаком приятной привычки.

        url = reverse("habits:habits_create")

        data3 = {
            "owner": self.user.pk,
            "place": "Автомобиль",
            "time": "8:20:00",
            "action": "Осмотр автомобиля",
            "is_nice": False,
            "related": self.habit_nice_false,
            "duration": 5,
            "periodicity": 1,
        }
        response = self.client.post(url, data=data3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_habit(self):
        """Тестирование вывода всех привычек"""

        url = reverse("habits:habits_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(2, data.get("count"))

    def test_retrieve_habit(self):
        """Тестирование просмотра одной привычки"""

        url = reverse("habits:habits_retrieve", args=(self.habit.pk,))  #
        print(f"Значение pk= {self.habit.pk}")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("owner"), self.habit.owner.id)
        self.assertEqual(data.get("place"), self.habit.place)
        self.assertEqual(data.get("time"), self.habit.time)
        self.assertEqual(data.get("action"), self.habit.action)
        self.assertEqual(data.get("duration"), self.habit.duration)
        self.assertEqual(data.get("periodicity"), self.habit.periodicity)
        self.assertEqual(data.get("friday"), True)

    def test_update_habit(self):
        """Тестирование изменений привычки"""

        url = reverse(
            "habits:habits_update", args=(self.habit.pk,)
        )  # , args=(self.habit.pk,)
        data = {
            "owner": self.user.pk,
            "place": "Работа",
            "time": "10:00:00",
            "action": "Попить чай",
            "duration": 10,
            "periodicity": 1,
        }
        response = self.client.put(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("owner"), self.habit.owner.id)
        self.assertEqual(data.get("place"), "Работа")
        self.assertEqual(data.get("time"), "10:00:00")
        self.assertEqual(data.get("action"), "Попить чай")
        self.assertEqual(data.get("duration"), 10)
        self.assertEqual(data.get("periodicity"), 1)
        self.assertEqual(data.get("is_nice"), True)
        self.assertEqual(data.get("sunday"), True)

    def test_delete_habit(self):
        """Тестирование удаления привычки"""

        url = reverse("habits:habits_delete", args=(self.habit.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_public_habit(self):
        """Тестирование вывода публичных привычек"""

        url = reverse("habits:public_list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, data.get("count"))
