# backend/sweets/models.py
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Sweet(models.Model):
    """
    Model representing a sweet/candy item in the shop.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)]
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.name
    
    def purchase(self, amount):
        """
        Decrease the quantity when a sweet is purchased.
        
        Args:
            amount (int): Number of items to purchase
            
        Raises:
            ValueError: If insufficient stock or invalid amount
        """
        if amount <= 0:
            raise ValueError("Purchase amount must be positive")
        
        if self.quantity < amount:
            raise ValueError(f"Insufficient stock. Only {self.quantity} available.")
        
        self.quantity -= amount
        self.save()
    
    def restock(self, amount):
        """
        Increase the quantity when restocking.
        
        Args:
            amount (int): Number of items to add to stock
            
        Raises:
            ValueError: If amount is not positive
        """
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        
        self.quantity += amount
        self.save()
    
    @property
    def is_in_stock(self):
        """Check if the sweet is currently in stock"""
        return self.quantity > 0