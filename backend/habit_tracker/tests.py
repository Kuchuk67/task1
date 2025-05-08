from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from habit_tracker.models import Habit
from users.models import CustomUser


class HabitTestCase(TestCase):
    """
    Тесты endpoint, permissions, validators
    """

    def setUp(self):
        self.client = APIClient()

        # Создание пользователя
        self.admin_user = CustomUser.objects.create(
            email="user@user.com",
            is_staff=True,
            is_superuser=True,
            nick_telegram="user",
            chat_id_telegram="12345",
        )
        self.admin_user.set_password("123456789")
        self.admin_user.save()

        self.user_1 = CustomUser.objects.create(
            email="user1@user.com",
            nick_telegram="user",
            chat_id_telegram="12345",
        )
        self.user_1.set_password("user1")
        self.user_1.save()

        self.client.force_authenticate(user=self.user_1)

        # Привычки

        self.habit1 = Habit.objects.create(
            user=self.user_1,
            place="Дома",
            action="Посмотреть стендап",
            time=10,
            public=False,
            nice=True
        )

        Habit.objects.create(
            user=self.user_1,
            place="Дома",
            action="Достать тренажер",
            time=30,
            public=True,
            related=self.habit1,
        )

        Habit.objects.create(
            user=self.admin_user,
            place="Спортзал",
            action="Выйти на тренировку",
            time=120,
            public=True,
        )
        Habit.objects.create(
            user=self.user_1,
            place="по дороге в офис",
            reward="купить кофе",
            action="Пройти мимо останоки",
            time=10,
            public=False,
        )

    def test_habit_list(self):
        response = self.client.get(reverse("habit:habit_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_habit_get(self):
        response = self.client.get(reverse("habit:habit-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_habit_post(self):
        fixture_data = dict({"place": "дом",
                             "time_action": "08:00:00",
                             "action": "действие",
                             "nice": True,
                             "related": None,
                             "reward": None,
                             "time": 1,
                             "public": False,
                             "user": 1,
                             "period": "1,2,4"
                             })
        data_response = dict({'place': 'дом',
                              'time_action': '08:00:00',
                              'action': 'действие',
                              'nice': True,
                              'related': None,
                              'period': '1,2,4',
                              'reward': None,
                              'time': 1,
                              'public': False,
                              'user': self.user_1.pk
                              })
        url = "/api/v1/habit"
        response = self.client.post(
            path=url,
            data=fixture_data,
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), data_response)

    def test_habit_validator_1(self):
        """
        Проверка валидаторов
        """
        fixture_data = dict({"place": "дом",
                             "time_action": "08:00:00",
                             "action": "действие",
                             "nice": True,
                             "related": None,
                             "reward": None,
                             "time": 1,
                             "public": False,
                             "user": 1,
                             "period": "1,2,4"
                             })
        url = "/api/v1/habit"

        """
        У приятной привычки не может быть
        вознаграждения или связанной привычки.
        """
        fixture_data["reward"] = "reward"
        response = self.client.post(
            path=url,
            data=fixture_data,
            format="json",
        )
        self.assertEqual(response.status_code, 422)

        """
        Исключить одновременный выбор связанной привычки
        и указания вознаграждения.
        """
        fixture_data["reward"] = "reward"
        fixture_data["related"] = self.habit1.pk
        fixture_data["nice"] = False

        response = self.client.post(
            path=url,
            data=fixture_data,
            format="json",
        )
        self.assertEqual(response.status_code, 422)

        """
        Время выполнения должно быть не больше 120 секунд.
        """
        fixture_data["related"] = None
        fixture_data["time"] = 121
        response = self.client.post(
            path=url,
            data=fixture_data,
            format="json",
        )
        self.assertEqual(response.status_code, 422)

        """
        Нельзя выполнять привычку реже,
        чем 1 раз в 7 дней.
        """

        fixture_data["period"] = "erfef"
        fixture_data["time"] = 60
        response = self.client.post(
            path=url,
            data=fixture_data,
            format="json",
        )
        self.assertEqual(response.status_code, 422)

        fixture_data["period"] = "1,2,8"
        fixture_data["time"] = 60
        response = self.client.post(
            path=url,
            data=fixture_data,
            format="json",
        )
        self.assertEqual(response.status_code, 422)
