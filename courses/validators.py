from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def validate_video_url(value):
    """Проверяет, что ссылка ведет на youtube.com."""
    if isinstance(value, dict):
        raise ValidationError('Ожидалась строка, но получен словарь.')
    parsed_url = urlparse(value)
    if parsed_url.netloc not in ['www.youtube.com', 'youtube.com']:
        raise ValidationError('Ссылки на сторонние ресурсы, кроме youtube.com, недопустимы.')