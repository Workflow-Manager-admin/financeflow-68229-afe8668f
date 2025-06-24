from rest_framework import serializers
from .models import Expense, Category


# PUBLIC_INTERFACE
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    Shows the category name and id, and (optional) user/owner info.
    """
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'user']
        read_only_fields = ['id', 'user']

# PUBLIC_INTERFACE


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for Expense model.
    Handles nested or PK display of category; exposes all necessary fields for the API/frontend.
    """
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )

    class Meta:
        model = Expense
        fields = [
            'id', 'user', 'category', 'category_id',
            'amount', 'description', 'date', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'category')

    # PUBLIC_INTERFACE
    def create(self, validated_data):
        """
        Creates a new Expense instance with nested category assignment.
        """
        return Expense.objects.create(**validated_data)

    # PUBLIC_INTERFACE
    def update(self, instance, validated_data):
        """
        Updates an Expense instance. Handles updating nested fields.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
