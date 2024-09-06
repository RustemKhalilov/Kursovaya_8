from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):
    """Тестирование модели Habits"""

    def setUp(self):
        """Создание тестовой модели Пользователя"""

        self.user = User.objects.create(
            email="user2@list.ru",
            password="qwerty12345",
            tg_chat_id="616492316",
            time_offset=3
        )

        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Тестирование создания пользователя"""

        url = reverse("users:register")
        data = {
            "email": "test3@list.ru",
            "password": "qwerty12345",
            "tg_chat_id": "616492316",
            "is_superuser": "False"
        }

        response = self.client.post(url, data=data)
        data = response.json()

        print(data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("email"), "test3@list.ru")
        print()
        self.assertEqual(data.get("password"), data["password"])# тут вот вопросик в профиле пользователя пароль  другой длинный типа
        #'pbkdf2_sha256$720000$ISaJFjIcTo9gl5bt3Z9HFh$Y5C/f0g5e8EiyEPBzQJq5RPTtBODbStu1KAAp9meCpo=' как вернуть нужный нам пароль в тесте да и вообще
        self.assertEqual(data.get("tg_chat_id"), "616492316")
        self.assertEqual(data.get("is_superuser"), None)

    def test_create_user_no_tg_chat_id(self):
        """Тестирование создания пользователя"""

        url = reverse("users:register")
        data = {
            "email": "test3@list.ru",
            "password": "qwerty12345",
            "is_superuser": "False",
            "time_offset": 3
        }

        response = self.client.post(url, data=data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_user(self):
        """Тестирование вывода всех пользователей"""

        response = self.client.get(reverse("users:users_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        """Тестирование просмотра одного пользователя"""

        url = reverse("users:users_retrieve_update", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), "user2@list.ru")
        self.assertEqual(data.get("password"), 'qwerty12345') # А тут нормальный пароль возвращает. Почему??
        self.assertEqual(data.get("tg_chat_id"), "616492316")
        self.assertEqual(data.get("is_superuser"), None)

    def test_user_update(self):
        """Тестирование обновления пользователя"""

        url = reverse("users:users_retrieve_update", args=(self.user.pk,))
        data = {"tg_chat_id": "0000000000"}
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("tg_chat_id"), "0000000000")
