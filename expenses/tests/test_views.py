import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestViews:
    """Тесты представлений"""
    
    def test_home_view(self, client):
        """Тест главной страницы"""
        response = client.get(reverse('home'))
        assert response.status_code == 200
        assert 'Контролируйте свои финансы' in response.content.decode()
    
    def test_expense_list_view(self, client, multiple_expenses):
        """Тест списка расходов"""
        response = client.get(reverse('expense-list'))
        assert response.status_code == 200
        assert len(response.context['expenses']) == 5
    
    def test_expense_detail_view(self, client, expense):
        """Тест деталей расхода"""
        response = client.get(reverse('expense-detail', args=[expense.id]))
        assert response.status_code == 200
    
    def test_expense_create_requires_login(self, client):
        """Тест что создание требует авторизации"""
        response = client.get(reverse('expense-create'))
        assert response.status_code == 302  # Редирект на логин
        assert '/login/' in response.url
    
    def test_expense_create_authenticated(self, authenticated_client, user):
        """Тест создания расхода авторизованным"""
        response = authenticated_client.post(reverse('expense-create'), {
            'title': 'Новый расход',
            'amount': '1500.50'
        })
        
        assert response.status_code == 302  # Редирект
        
        from expenses.models import Expense
        assert Expense.objects.filter(title='Новый расход').exists()
    
    def test_login_view(self, client):
        """Тест страницы входа"""
        response = client.get(reverse('login'))
        assert response.status_code == 200
    
    def test_register_view(self, client):
        """Тест страницы регистрации"""
        response = client.get(reverse('register'))
        assert response.status_code == 200
    
    def test_user_registration(self, client):
        """Тест регистрации пользователя"""
        from django.contrib.auth.models import User
        
        response = client.post(reverse('register'), {
            'username': 'newuser123',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!'
        })
        
        assert response.status_code == 302  # Редирект после успешной регистрации
        assert User.objects.filter(username='newuser123').exists()