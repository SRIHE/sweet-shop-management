# backend/authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model with additional fields for the sweet shop.
    """
    is_admin = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    
    # Make email required for authentication
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'