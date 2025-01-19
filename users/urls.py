from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, PaymentViewSet, UserRegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'profile', UserProfileViewSet, basename='user')
router.register(r'register', UserRegisterView, basename='register')

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
