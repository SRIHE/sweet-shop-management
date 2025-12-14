# backend/sweets/tests/test_models.py
import pytest
from django.contrib.auth import get_user_model
from decimal import Decimal
from sweets.models import Sweet

User = get_user_model()

@pytest.mark.django_db
class TestSweetModel:
    
    def test_create_sweet_with_valid_data(self):
        """Test creating a sweet with all required fields"""
        sweet = Sweet.objects.create(
            name="Chocolate Bar",
            category="Chocolate",
            price=Decimal("2.50"),
            quantity=100
        )
        
        assert sweet.name == "Chocolate Bar"
        assert sweet.category == "Chocolate"
        assert sweet.price == Decimal("2.50")
        assert sweet.quantity == 100
        assert sweet.id is not None
    
    def test_sweet_string_representation(self):
        """Test the string representation of a sweet"""
        sweet = Sweet.objects.create(
            name="Gummy Bears",
            category="Gummy",
            price=Decimal("1.99"),
            quantity=50
        )
        
        assert str(sweet) == "Gummy Bears"
    
    def test_sweet_cannot_have_negative_price(self):
        """Test that sweet price cannot be negative"""
        with pytest.raises(Exception):
            Sweet.objects.create(
                name="Invalid Sweet",
                category="Test",
                price=Decimal("-1.00"),
                quantity=10
            )
    
    def test_sweet_cannot_have_negative_quantity(self):
        """Test that sweet quantity cannot be negative"""
        with pytest.raises(Exception):
            Sweet.objects.create(
                name="Invalid Sweet",
                category="Test",
                price=Decimal("2.00"),
                quantity=-5
            )
    
    def test_sweet_has_timestamps(self):
        """Test that sweet has created_at and updated_at timestamps"""
        sweet = Sweet.objects.create(
            name="Lollipop",
            category="Hard Candy",
            price=Decimal("0.99"),
            quantity=200
        )
        
        assert sweet.created_at is not None
        assert sweet.updated_at is not None
    
    def test_purchase_decreases_quantity(self):
        """Test purchasing a sweet decreases its quantity"""
        sweet = Sweet.objects.create(
            name="Candy Cane",
            category="Seasonal",
            price=Decimal("1.50"),
            quantity=10
        )
        
        initial_quantity = sweet.quantity
        sweet.purchase(3)
        
        assert sweet.quantity == initial_quantity - 3
    
    def test_purchase_raises_error_if_insufficient_stock(self):
        """Test that purchasing more than available raises an error"""
        sweet = Sweet.objects.create(
            name="Limited Edition",
            category="Special",
            price=Decimal("5.00"),
            quantity=2
        )
        
        with pytest.raises(ValueError, match="Insufficient stock"):
            sweet.purchase(5)
    
    def test_restock_increases_quantity(self):
        """Test restocking increases quantity"""
        sweet = Sweet.objects.create(
            name="Marshmallow",
            category="Soft Candy",
            price=Decimal("3.00"),
            quantity=5
        )
        
        initial_quantity = sweet.quantity
        sweet.restock(20)
        
        assert sweet.quantity == initial_quantity + 20
    
    def test_restock_cannot_add_negative_quantity(self):
        """Test that restocking with negative quantity raises error"""
        sweet = Sweet.objects.create(
            name="Taffy",
            category="Chewy",
            price=Decimal("2.25"),
            quantity=15
        )
        
        with pytest.raises(ValueError, match="Restock amount must be positive"):
            sweet.restock(-5)