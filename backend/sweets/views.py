# backend/sweets/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Sweet
from .serializers import SweetSerializer, PurchaseSerializer, RestockSerializer
from .permissions import IsAdminOrReadOnly, IsAdmin

class SweetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing sweets
    """
    queryset = Sweet.objects.all()
    serializer_class = SweetSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_permissions(self):
        """
        Custom permissions based on action
        """
        if self.action in ['destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return super().get_permissions()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def search(self, request):
        """
        Search for sweets by name, category, or price range
        Query params: name, category, min_price, max_price
        """
        queryset = self.get_queryset()
        
        name = request.query_params.get('name', None)
        category = request.query_params.get('category', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        if min_price:
            try:
                queryset = queryset.filter(price__gte=float(min_price))
            except ValueError:
                return Response(
                    {'error': 'Invalid min_price value'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        if max_price:
            try:
                queryset = queryset.filter(price__lte=float(max_price))
            except ValueError:
                return Response(
                    {'error': 'Invalid max_price value'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def purchase(self, request, pk=None):
        """
        Purchase a sweet - decreases quantity
        """
        sweet = self.get_object()
        serializer = PurchaseSerializer(data=request.data)
        
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            
            try:
                sweet.purchase(amount)
                return Response({
                    'message': f'Successfully purchased {amount} {sweet.name}(s)',
                    'remaining_quantity': sweet.quantity
                }, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def restock(self, request, pk=None):
        """
        Restock a sweet - increases quantity (Admin only)
        """
        sweet = self.get_object()
        serializer = RestockSerializer(data=request.data)
        
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            
            try:
                sweet.restock(amount)
                return Response({
                    'message': f'Successfully restocked {amount} {sweet.name}(s)',
                    'new_quantity': sweet.quantity
                }, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response(
                    {'error': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)