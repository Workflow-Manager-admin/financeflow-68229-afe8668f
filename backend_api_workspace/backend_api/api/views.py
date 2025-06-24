from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from .models import Expense, Category
from .serializers import (
    ExpenseSerializer,
    CategorySerializer,
    ExpenseSummarySerializer,
    RegisterSerializer,
    LoginSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import login, logout
from django.db import models


@api_view(['GET'])
def health(request):
    return Response({"message": "Server is up!"})


class IsOwnerPermission(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to access or edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class RegisterAPIView(generics.CreateAPIView):
    """
    POST: Register a new user.
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class LoginAPIView(APIView):
    """
    POST: Login user and get token.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": user.username}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
    POST: Logout user (delete token).
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, updating, and deleting expenses.
    Filtering and searching by category, date, description, and amount.
    Only returns and allows access to objects for the logged-in user.
    """
    serializer_class = ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'date']
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related('category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, creating, updating, and deleting categories.
    Only allows actions on categories belonging to the logged-in user.
    """
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class DashboardSummaryAPIView(APIView):
    """
    Returns summary info for expense dashboard:
    - Total expenses for user
    - Breakdown by category
    - Number of expenses
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        expenses = Expense.objects.filter(user=request.user)
        total = expenses.aggregate(total=models.Sum('amount'))['total'] or 0
        by_category_qs = expenses.values('category__name').annotate(total=models.Sum('amount'))
        by_category = {
            c['category__name'] if c['category__name'] else 'Uncategorized': c['total']
            for c in by_category_qs
        }
        count = expenses.count()
        serializer = ExpenseSummarySerializer(
            {"total_expenses": total, "by_category": by_category, "count": count}
        )
        return Response(serializer.data, status=200)
