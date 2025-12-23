import pytest
from django.urls import reverse, resolve


@pytest.mark.django_db
class TestURLs:
    """Тесты URL маршрутов"""
    
    def test_home_url(self):
        """Тест URL главной страницы"""
        url = reverse('home')
        assert url == '/'
    
    def test_expense_list_url(self):
        """Тест URL списка расходов"""
        url = reverse('expense-list')
        assert url == '/expenses/'
    
    def test_expense_create_url(self):
        """Тест URL создания расхода"""
        url = reverse('expense-create')
        assert url == '/expenses/create/'
    
    def test_expense_detail_url(self):
        """Тест URL деталей расхода"""
        url = reverse('expense-detail', args=[1])
        assert url == '/expenses/1/'
    
    def test_login_url(self):
        """Тест URL входа"""
        url = reverse('login')
        assert url == '/login/'
    
    def test_register_url(self):
        """Тест URL регистрации"""
        url = reverse('register')
        assert url == '/register/'
    
    def test_all_urls_exist(self):
        """Тест что все URL существуют"""
        urls_to_test = [
            ('home', []),
            ('expense-list', []),
            ('expense-create', []),
            ('expense-detail', [1]),
            ('expense-update', [1]),
            ('expense-delete', [1]),
            ('login', []),
            ('logout', []),
            ('register', []),
        ]
        
        for url_name, args in urls_to_test:
            try:
                reverse(url_name, args=args if args else None)
            except Exception as e:
                pytest.fail(f"URL {url_name} не существует: {e}")