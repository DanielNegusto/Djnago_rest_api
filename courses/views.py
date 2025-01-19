from rest_framework import viewsets
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.
    Позволяет создавать, обновлять, частично обновлять, удалять и просматривать курсы.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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
        иначе возвращает только курсы, принадлежащие текущему пользователю.
        """
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        """
        Сохраняет новый курс с указанием владельца.
        """
        serializer.save(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления уроками.
    Позволяет создавать, обновлять, частично обновлять, удалять и просматривать уроки.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

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
