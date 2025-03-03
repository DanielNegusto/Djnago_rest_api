from celery import shared_task
from django.utils import timezone
from .models import User
from datetime import timedelta


@shared_task
def check_inactive_users():
    month_ago = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(last_login__lt=month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f"User  {user.email} has been deactivated.")
