from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method']


class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'password', 'payments']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # Хешируем пароль
        return super().create(validated_data)
