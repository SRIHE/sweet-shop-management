import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from sweets.models import Sweet
from decimal import Decimal

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create_user(**kwargs)
    return make_user

@pytest.fixture
def create_admin_user(db):
    def make_admin(**kwargs):
        user = User.objects.create_user(**kwargs)
        user.is_admin = True
        user.save()
        return user
    return make_admin

@pytest.fixture
def create_sweet(db):
    def make_sweet(**kwargs):
        defaults = {
            'name': 'Test Sweet',
            'category': 'Test',
            'price': Decimal('10.00'),
            'quantity': 50
        }
        defaults.update(kwargs)
        return Sweet.objects.create(**defaults)
    return make_sweet

@pytest.mark.django_db
class TestAuthenticationViews:
    
    def test_user_registration(self, api_client):
        """Test user can register successfully"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        response = api_client.post('/api/auth/register/', data)
        assert response.status_code == 201
        assert 'tokens' in response.data
        assert 'user' in response.data
    
    def test_user_login(self, api_client, create_user):
        """Test user can login successfully"""
        user = create_user(username='testuser', email='test@example.com', password='testpass123')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == 200
        assert 'tokens' in response.data
    
    def test_login_with_invalid_credentials(self, api_client):
        """Test login fails with wrong password"""
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = api_client.post('/api/auth/login/', data)
        assert response.status_code == 401

@pytest.mark.django_db
class TestSweetViews:
    
    def test_list_sweets_authenticated(self, api_client, create_user, create_sweet):
        """Test authenticated user can list sweets"""
        user = create_user(username='testuser', email='test@example.com', password='testpass123')
        create_sweet(name='Chocolate Bar')
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/sweets/')
        assert response.status_code == 200
        assert len(response.data) > 0
    
    def test_list_sweets_unauthenticated(self, api_client):
        """Test unauthenticated user cannot list sweets"""
        response = api_client.get('/api/sweets/')
        assert response.status_code == 401
    
    def test_create_sweet_as_admin(self, api_client, create_admin_user):
        """Test admin can create sweets"""
        admin = create_admin_user(username='admin', email='admin@test.com', password='admin123')
        api_client.force_authenticate(user=admin)
        data = {
            'name': 'New Sweet',
            'category': 'Chocolate',
            'price': '25.50',
            'quantity': 100
        }
        response = api_client.post('/api/sweets/', data)
        assert response.status_code == 201
        assert response.data['name'] == 'New Sweet'
    
    def test_create_sweet_as_regular_user(self, api_client, create_user):
        """Test regular user cannot create sweets"""
        user = create_user(username='testuser', email='test@example.com', password='testpass123')
        api_client.force_authenticate(user=user)
        data = {
            'name': 'New Sweet',
            'category': 'Chocolate',
            'price': '25.50',
            'quantity': 100
        }
        response = api_client.post('/api/sweets/', data)
        assert response.status_code == 403
    
    def test_search_sweets_by_name(self, api_client, create_user, create_sweet):
        """Test searching sweets by name"""
        user = create_user(username='testuser', email='test@example.com', password='testpass123')
        create_sweet(name='Chocolate Bar', category='Chocolate')
        create_sweet(name='Gummy Bears', category='Gummy')
        api_client.force_authenticate(user=user)
        response = api_client.get('/api/sweets/search/?name=Chocolate')
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]['name'] == 'Chocolate Bar'
    
    def test_purchase_sweet(self, api_client, create_user, create_sweet):
        """Test purchasing a sweet decreases quantity"""
        user = create_user(username='testuser', email='test@example.com', password='testpass123')
        sweet = create_sweet(name='Test Sweet', quantity=50)
        api_client.force_authenticate(user=user)
        response = api_client.post(f'/api/sweets/{sweet.id}/purchase/', {'amount': 5})
        assert response.status_code == 200
        sweet.refresh_from_db()
        assert sweet.quantity == 45
    
    def test_purchase_insufficient_stock(self, api_client, create_user, create_sweet):
        """Test purchasing more than available stock fails"""
        user = create_user(username='testuser', email='test@example.com', password='testpass123')
        sweet = create_sweet(name='Test Sweet', quantity=5)
        api_client.force_authenticate(user=user)
        response = api_client.post(f'/api/sweets/{sweet.id}/purchase/', {'amount': 10})
        assert response.status_code == 400
    
    def test_restock_sweet_as_admin(self, api_client, create_admin_user, create_sweet):
        """Test admin can restock sweets"""
        admin = create_admin_user(username='admin', email='admin@test.com', password='admin123')
        sweet = create_sweet(name='Test Sweet', quantity=10)
        api_client.force_authenticate(user=admin)
        response = api_client.post(f'/api/sweets/{sweet.id}/restock/', {'amount': 20})
        assert response.status_code == 200
        sweet.refresh_from_db()
        assert sweet.quantity == 30
    
    def test_restock_sweet_as_regular_user(self, api_client, create_user, create_sweet):
        """Test regular user cannot restock sweets"""
        user = create_user(username='testuser', email='test@example.com', password='testpass123')
        sweet = create_sweet(name='Test Sweet', quantity=10)
        api_client.force_authenticate(user=user)
        response = api_client.post(f'/api/sweets/{sweet.id}/restock/', {'amount': 20})
        assert response.status_code == 403
    
    def test_delete_sweet_as_admin(self, api_client, create_admin_user, create_sweet):
        """Test admin can delete sweets"""
        admin = create_admin_user(username='admin', email='admin@test.com', password='admin123')
        sweet = create_sweet(name='Test Sweet')
        api_client.force_authenticate(user=admin)
        response = api_client.delete(f'/api/sweets/{sweet.id}/')
        assert response.status_code == 204
        assert Sweet.objects.filter(id=sweet.id).count() == 0