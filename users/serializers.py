from rest_framework import serializers
from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Payment.
    Позволяет преобразовывать данные о платежах в JSON и обратно.
    """

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_date",
            "paid_course",
            "paid_lesson",
            "amount",
            "payment_method",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователей.
    Позволяет создать нового пользователя с указанием email и пароля.
    """

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Создает нового пользователя с заданными данными.
        """
        password = validated_data.pop("password", None)
        if password is None:
            raise serializers.ValidationError({"password": "Password is required."})
        user = User.objects.create_user(**validated_data, password=password)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Сериализатор для профиля пользователя.
    Позволяет обновлять данные пользователя и включать информацию о платежах.
    """

    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "payments", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def update(self, instance, validated_data):
        """
        Обновляет данные пользователя, включая возможность изменения пароля.
        """
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance


class UserProfileReadOnlySerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения профиля пользователя без чувствительных данных.
    """

    class Meta:
        model = User
        fields = ["id", "email"]
