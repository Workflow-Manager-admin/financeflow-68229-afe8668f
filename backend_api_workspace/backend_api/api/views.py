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


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="get",
    operation_summary="Health Check",
    operation_description="Check if the server is up and reachable.",
    responses={
        200: openapi.Response(
            description="A successful response",
            examples={"application/json": {"message": "Server is up!"}}
        )
    },
    tags=["Health"]
)
@api_view(['GET'])
def health(request):
    """
    Health check endpoint.

    Returns:
        200 OK: {"message": "Server is up!"}
    """
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

    Registers a user with username and password and returns the user ID and username.

    - Returns 201 Created and the created user fields on success.
    - Request body: {"username": "...", "password": "..."}
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Register",
        operation_description="Register a new user. Returns user details.",
        tags=["Auth"],
        responses={201: openapi.Response('Created', RegisterSerializer), 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        """Create user and return user info."""
        return super().post(request, *args, **kwargs)


class LoginAPIView(APIView):
    """
    POST: Login user and get token.

    Authenticates a user given username and password.
    Returns a token on successful login.

    - Request body: {"username": "...", "password": "..."}
    - Response: {"token": "<token>", "user": "<username>"}
    """
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Login",
        operation_description="Login user and get authentication token.",
        tags=["Auth"],
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(
                'Token',
                openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'token': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Authentication token'
                        ),
                        'user': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='Username'
                        ),
                    }
                )
            ),
            400: 'Invalid credentials'
        }
    )
    def post(self, request):
        """
        Authenticate and return a token if credentials are valid.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user": user.username},
            status=status.HTTP_200_OK
        )


class LogoutAPIView(APIView):
    """
    POST: Logout user (delete token).

    Revokes the user's authentication token, effectively logging them out.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Logout",
        operation_description="Logout the authenticated user (token revoked). Requires authentication.",
        tags=["Auth"],
        responses={
            204: 'Logged out successfully',
            401: 'Authentication credentials were not provided or invalid'
        }
    )
    def post(self, request):
        """
        Deletes the user's auth token and logs out.
        """
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Expense API

    API endpoint for listing, creating, updating, and deleting expenses.

    - List your expenses (with filtering/search on category, description, date, amount)
    - CRUD (Create, Retrieve, Update, Delete) for expenses (user-scoped)
    - Requires authentication via Token
    - Only returns/edits expenses belonging to user

    Filtering:
    - filterset_fields: category, date
    - search_fields: description, category__name
    - ordering_fields: date, amount, created_at

    Security:
    - Only objects belonging to the authenticated user are visible/mutable.
    """
    serializer_class = ExpenseSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'date']
    search_fields = ['description', 'category__name']
    ordering_fields = ['date', 'amount', 'created_at']

    @swagger_auto_schema(
        operation_summary="List Expenses",
        operation_description="List all expenses for the authenticated user. Supports filtering and searching.",
        tags=["Expenses"],
        responses={200: ExpenseSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List expenses for the authenticated user."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Expense",
        operation_description="Create a new expense for the authenticated user.",
        tags=["Expenses"],
        responses={201: ExpenseSerializer}
    )
    def create(self, request, *args, **kwargs):
        """Create a new expense."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Expense",
        operation_description="Get details of a single expense by ID (must belong to user).",
        tags=["Expenses"],
        responses={200: ExpenseSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single expense."""
        return super().retrieve(request, *args, **kwargs)

    update_expense_doc = (
        "Update details for an existing expense "
        "(must belong to user)."
    )
    @swagger_auto_schema(
        operation_summary="Update Expense",
        operation_description=update_expense_doc,
        tags=["Expenses"],
        responses={200: ExpenseSerializer}
    )
    def update(self, request, *args, **kwargs):
        """Update an expense."""
        return super().update(request, *args, **kwargs)

    partial_update_expense_doc = (
        "Partially update an existing expense "
        "(must belong to user)."
    )
    @swagger_auto_schema(
        operation_summary="Partial Update Expense",
        operation_description=partial_update_expense_doc,
        tags=["Expenses"],
        responses={200: ExpenseSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update an expense."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Expense",
        operation_description="Delete an expense (must belong to user).",
        tags=["Expenses"],
        responses={204: 'Deleted'}
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an expense."""
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).select_related('category')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category API

    API endpoint for listing, creating, updating, and deleting categories.

    - List your categories (with search)
    - CRUD (Create, Retrieve, Update, Delete) for categories (user-scoped)
    - Requires authentication via Token
    - Only categories belonging to the authenticated user are visible/mutable

    Filtering:
    - filterset_fields: name
    - search_fields: name

    Security:
    - Only objects belonging to the authenticated user are visible/mutable.
    """
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwnerPermission]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name']

    @swagger_auto_schema(
        operation_summary="List Categories",
        operation_description="List all categories for the authenticated user. Supports search.",
        tags=["Categories"],
        responses={200: CategorySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """List categories for the authenticated user."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Category",
        operation_description="Create a new category for the authenticated user.",
        tags=["Categories"],
        responses={201: CategorySerializer}
    )
    def create(self, request, *args, **kwargs):
        """Create a new category."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Retrieve Category",
        operation_description="Get details of a single category by ID (must belong to user).",
        tags=["Categories"],
        responses={200: CategorySerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a single category."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update Category",
        operation_description="Update details for an existing category (must belong to user).",
        tags=["Categories"],
        responses={200: CategorySerializer}
    )
    def update(self, request, *args, **kwargs):
        """Update a category."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Partial Update Category",
        operation_description="Partially update an existing category (must belong to user).",
        tags=["Categories"],
        responses={200: CategorySerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        """Partially update a category."""
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Delete Category",
        operation_description="Delete a category (must belong to user).",
        tags=["Categories"],
        responses={204: 'Deleted'}
    )
    def destroy(self, request, *args, **kwargs):
        """Delete a category."""
        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class DashboardSummaryAPIView(APIView):
    """
    Dashboard/summary API.

    Returns summary info for expense dashboard:
    - Total expenses for user
    - Breakdown by category
    - Number of expenses

    Requires authentication via Token.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Dashboard Summary",
        operation_description=(
            "Return dashboard summary: total expenses, breakdown by category, "
            "and count for authenticated user."
        ),
        tags=["Dashboard"],
        responses={
            200: openapi.Response(
                "Summary",
                ExpenseSummarySerializer,
                examples={
                    "application/json": {
                        "total_expenses": "1000.00",
                        "by_category": {
                            "Food": "500.00",
                            "Transport": "200.00",
                            "Uncategorized": "300.00"
                        },
                        "count": 10
                    }
                }
            )
        }
    )
    def get(self, request):
        """
        Returns expense summary for the authenticated user for dashboard.
        """
        expenses = Expense.objects.filter(user=request.user)
        total = expenses.aggregate(total=models.Sum('amount'))['total'] or 0
        by_category_qs = expenses.values('category__name').annotate(
            total=models.Sum('amount')
        )
        by_category = {
            c['category__name'] if c['category__name']
            else 'Uncategorized': c['total']
            for c in by_category_qs
        }
        count = expenses.count()
        serializer = ExpenseSummarySerializer(
            {"total_expenses": total, "by_category": by_category, "count": count}
        )
        return Response(serializer.data, status=200)
