from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    for subscriber in subscribers:
        send_mail(
            subject=f'Обновление курса: {course.title}',
            message=f'Курс "{course.title}" был обновлен. Проверьте новые материалы!',
            from_email='your_email@example.com',
            recipient_list=[subscriber.user.email],
        )