# backend/sweets/serializers.py
from rest_framework import serializers
from .models import Sweet

class SweetSerializer(serializers.ModelSerializer):
    """Serializer for Sweet model"""
    is_in_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Sweet
        fields = [
            'id', 'name', 'category', 'price', 'quantity',
            'description', 'is_in_stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_price(self, value):
        """Ensure price is positive"""
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero")
        return value
    
    def validate_quantity(self, value):
        """Ensure quantity is non-negative"""
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value


class PurchaseSerializer(serializers.Serializer):
    """Serializer for purchasing sweets"""
    amount = serializers.IntegerField(min_value=1)
    
    def validate_amount(self, value):
        """Validate purchase amount"""
        if value <= 0:
            raise serializers.ValidationError("Purchase amount must be positive")
        return value


class RestockSerializer(serializers.Serializer):
    """Serializer for restocking sweets"""
    amount = serializers.IntegerField(min_value=1)
    
    def validate_amount(self, value):
        """Validate restock amount"""
        if value <= 0:
            raise serializers.ValidationError("Restock amount must be positive")
        return value