from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Course, Lesson, Subscription
from .paginators import CustomPageNumberPagination
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated
from .tasks import send_course_update_email


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.
    Позволяет создавать, обновлять, частично обновлять, удалять и просматривать курсы.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        """
        Определяет разрешения для действий в зависимости от типа действия.
        """
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает список курсов в зависимости от прав пользователя.
        Если пользователь является модератором, возвращает все курсы,
        иначе возвращает только курсы, принадлежащие текущему пользователю
        или на которые он подписан.
        """
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Course.objects.all()

        subscribed_courses = Course.objects.filter(subscription__user=user)
        user_courses = Course.objects.filter(owner=user)

        return user_courses | subscribed_courses

    def perform_create(self, serializer):
        """
        Сохраняет новый курс с указанием владельца.
        """
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()

            print(f"Отправка уведомления для курса {instance.id}")
            send_course_update_email.delay(instance.id)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления уроками.
    Позволяет создавать, обновлять, частично обновлять, удалять и просматривать уроки.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        """
        Определяет разрешения для действий в зависимости от типа действия.
        """
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает список уроков в зависимости от прав пользователя.
        Если пользователь является модератором, возвращает все уроки,
        иначе возвращает только уроки, принадлежащие текущему пользователю.
        """
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Сохраняет новый урок с указанием владельца.
        """
        serializer.save(owner=self.request.user)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)
