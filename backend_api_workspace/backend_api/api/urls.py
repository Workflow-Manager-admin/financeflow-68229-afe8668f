from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    health,
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ExpenseViewSet,
    CategoryViewSet,
    DashboardSummaryAPIView
)

router = DefaultRouter()
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('health/', health, name='Health'),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('dashboard/summary/', DashboardSummaryAPIView.as_view(), name='dashboard-summary'),
    path('', include(router.urls)),
]
