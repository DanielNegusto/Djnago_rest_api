from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from .models import Course, Lesson, Subscription


class LessonAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="password")
        self.moderator = User.objects.create_user(
            email="moderator@test.com", password="password"
        )
        self.moderator.groups.create(name="Moderators")

        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson Description",
            course=self.course,
        )

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = "http://localhost:8000/api/lessons/"
        data = {
            "title": "New Lesson",
            "description": "New Lesson Description",
            "course": self.course.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = f"http://localhost:8000/api/lessons/{self.lesson.id}/"
        data = {
            "title": "Updated Lesson Title",
            "description": "Updated Lesson Description",
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson Title")

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = f"http://localhost:8000/api/lessons/{self.lesson.id}/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        url = "http://localhost:8000/api/subscriptions/"
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )

    def test_create_course(self):
        self.client.force_authenticate(user=self.user)
        url = "http://localhost:8000/api/courses/"
        data = {"title": "New Course", "description": "New Course Description"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
