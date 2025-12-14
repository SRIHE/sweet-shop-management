# backend/sweets/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SweetViewSet

router = DefaultRouter()
router.register(r'sweets', SweetViewSet, basename='sweet')

urlpatterns = [
    path('', include(router.urls)),
]