from django.contrib import admin
from .models import Sweet

@admin.register(Sweet)
class SweetAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'quantity', 'is_in_stock']
    list_filter = ['category']
    search_fields = ['name', 'category']