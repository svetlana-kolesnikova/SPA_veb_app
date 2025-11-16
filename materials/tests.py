# materials/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from users.models import CourseSubscription
from materials.models import Course, Lesson

User = get_user_model()

class LessonsAndSubscriptionTests(APITestCase):
    """
    Тесты для проверки функционала уроков, пагинации и подписок на курсы.
    """

    def setUp(self):
        """
        Создание тестовых данных:
        - пользователь,
        - курсы,
        - уроки,
        - подписки.
        """

        self.client = APIClient()
        # создаём двух пользователей
        self.user1 = User.objects.create_user(email="u1@example.com", password="pass12345")
        self.user2 = User.objects.create_user(email="u2@example.com", password="pass12345")

        # создаём курс и урок, owner = user1
        self.client.force_authenticate(self.user1)
        resp = self.client.post(reverse("materials:course-list"), {"name": "Test Course", "description": "desc"})
        self.assertIn(resp.status_code, (201, 200))
        self.course_id = resp.data["id"]

        # создаём урок с корректной ссылкой на youtube
        lesson_data = {
            "name": "Lesson 1",
            "description": "desc",
            "course": self.course_id,
            "video_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
        resp = self.client.post(reverse("materials:lesson-list-create"), lesson_data, format="json")
        self.assertEqual(resp.status_code, 201)
        self.lesson_id = resp.data["id"]

        self.client.force_authenticate(None)

    def test_create_lesson_disallow_non_youtube(self):
        """
        Проверка корректной работы пагинации при выводе списка уроков
        """

        self.client.force_authenticate(self.user1)
        bad = {
            "name": "Bad",
            "course": self.course_id,
            "video_link": "https://some-edu-platform.com/course/abc"
        }
        resp = self.client.post(reverse("materials:lesson-list-create"), bad, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("video_link", resp.data)
        self.client.force_authenticate(None)

    def test_subscription_flow(self):
        """
        Проверка установки и удаления подписки пользователя на курс.
        После подписки поле is_subscribed для курса должно быть True.
        После удаления подписки — False.
        """

        # Добавляем подписку
        self.client.force_authenticate(self.user2)
        url = reverse("materials:course-subscribe", kwargs={"pk": self.course_id})
        resp = self.client.post(url)
        self.assertIn(resp.status_code, (201, 200))
        self.assertTrue(CourseSubscription.objects.filter(user=self.user2, course_id=self.course_id).exists())

        # Проверяем поле is_subscribed в сериализаторе курса
        resp = self.client.get(reverse("materials:course-detail", kwargs={"pk": self.course_id}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.data.get("is_subscribed", False))

        # Удаляем подписку
        url_un = reverse("materials:course-unsubscribe", kwargs={"pk": self.course_id})
        resp = self.client.post(url_un)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(CourseSubscription.objects.filter(user=self.user2, course_id=self.course_id).exists())

        self.client.force_authenticate(None)

    def test_lessons_pagination(self):
        """Тестирование пагинации"""

        self.client.force_authenticate(self.user1)
        for i in range(12):
            self.client.post(reverse("materials:lesson-list-create"), {
                "name": f"L{i}",
                "course": self.course_id,
                "video_link": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }, format="json")
        resp = self.client.get(reverse("materials:lesson-list-create"))
        self.assertEqual(resp.status_code, 200)

        self.assertIn("results", resp.data)
        self.client.force_authenticate(None)
