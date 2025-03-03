from django.core.management.base import BaseCommand
from users.models import Payment, User
from courses.models import Course, Lesson  # Импортируйте ваши модели Course и Lesson
from decimal import Decimal


class Command(BaseCommand):
    help = "Populate the Payment table with sample data"

    def handle(self, *args, **kwargs):
        # Создание или получение пользователей
        user1, created1 = User.objects.get_or_create(
            email="user1@example.com",  # Замените на желаемый email
            defaults={
                "phone": "1234567890",
                "city": "City1",
                "is_active": True,
                "is_staff": False,
            },
        )

        user2, created2 = User.objects.get_or_create(
            email="user2@example.com",  # Замените на желаемый email
            defaults={
                "phone": "0987654321",
                "city": "City2",
                "is_active": True,
                "is_staff": False,
            },
        )

        # Создание или получение курса
        course1, created_course = Course.objects.get_or_create(
            title="Course 1",  # Замените на желаемый заголовок курса
            defaults={
                "description": "Description for Course 1",
                # Добавьте другие поля курса, если необходимо
            },
        )

        lesson1, created_lesson = Lesson.objects.get_or_create(
            title="Lesson 1",  # Замените на желаемый заголовок урока
            defaults={
                "course": course1,
                "description": "Content for Lesson 1",
                # Добавьте другие поля урока, если необходимо
            },
        )

        # Создание записей в таблице Payment
        Payment.objects.create(
            user=user1,
            paid_course=course1,
            amount=Decimal("100.00"),
            payment_method="cash",
        )

        Payment.objects.create(
            user=user2,
            paid_lesson=lesson1,
            amount=Decimal("50.00"),
            payment_method="transfer",
        )

        self.stdout.write(self.style.SUCCESS("Payment table populated successfully!"))
