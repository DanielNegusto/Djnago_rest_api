from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r'profile', UserProfileViewSet, basename='user-profile')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]