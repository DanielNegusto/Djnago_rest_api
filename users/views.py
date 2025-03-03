from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters import rest_framework as filters
from courses.models import Lesson, Course
from .models import User, Payment
from .permissions import IsOwnerUser
from .serializers import (
    UserProfileSerializer,
    PaymentSerializer,
    UserRegisterSerializer,
    UserProfileReadOnlySerializer,
)
from rest_framework.response import Response

from .services import (
    save_payment,
    create_checkout_session,
    create_price,
    create_product,
)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления профилями пользователей.
    Позволяет просматривать, обновлять и частично обновлять профили пользователей.
    """

    queryset = User.objects.all()

    def get_permissions(self):
        """
        Определяет разрешения для действий в зависимости от типа действия.
        """
        if self.action in ["update", "partial_update"]:
            self.permission_classes = [IsAuthenticated, IsOwnerUser]
        else:
            self.permission_classes = [IsAuthenticated]

        return super().get_permissions()

    def get_serializer_class(self):
        """
        Возвращает соответствующий сериализатор в зависимости от типа действия.
        """
        if self.action == "list":
            return UserProfileReadOnlySerializer
        elif self.action == "retrieve":
            user_id = self.kwargs.get("pk")
            if str(user_id) == str(self.request.user.id):
                return UserProfileSerializer
            return UserProfileReadOnlySerializer
        return UserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Обрабатывает запрос на получение профиля пользователя.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Обрабатывает запрос на обновление профиля пользователя.
        """
        instance = self.get_object()
        serializer = UserProfileSerializer(instance, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(viewsets.ModelViewSet):
    """
    ViewSet для регистрации пользователей.
    Позволяет создавать новых пользователей.
    """

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """
        Обрабатывает запрос на создание нового пользователя.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # Сохранение пользователя
        return Response({"user_id": user.id}, status=status.HTTP_201_CREATED)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления платежами.
    Позволяет просматривать, создавать, обновлять и удалять платежи.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        "paid_course": ["exact"],
        "paid_lesson": ["exact"],
        "payment_method": ["exact"],
    }
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]

    def create(self, request, *args, **kwargs):
        """
        Создает новый платеж и сессию Stripe, возвращает URL для завершения оплаты.
        """
        course_id = request.data.get("paid_course")
        lesson_id = request.data.get("paid_lesson")
        amount = request.data.get("amount")

        course = Course.objects.get(id=course_id) if course_id else None
        lesson = Lesson.objects.get(id=lesson_id) if lesson_id else None

        product = create_product(course.id)

        price = create_price(product.id, amount)

        session = create_checkout_session(price.id)

        save_payment(
            user=request.user,
            course=course,
            lesson=lesson,
            amount=amount,
            session_id=session.id,
        )

        return Response({"url": session.url}, status=status.HTTP_201_CREATED)
