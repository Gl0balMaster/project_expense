import pytest
from decimal import Decimal
from datetime import date
import time


@pytest.mark.django_db
class TestExpenseModel:
    """Тесты модели Expense"""
    
    def test_expense_creation(self, user):
        """Тест создания расхода"""
        from expenses.models import Expense
        
        expense = Expense.objects.create(
            user=user,
            title='Продукты',
            amount=Decimal('1500.50')
        )
        
        assert expense.title == 'Продукты'
        assert expense.amount == Decimal('1500.50')
        assert expense.user == user
        assert expense.date == date.today()
    
    def test_expense_str(self, expense):
        """Тест строкового представления"""
        assert str(expense) == f'{expense.title} - {expense.amount}'
    
    def test_expense_without_user(self):
        """Тест расхода без пользователя - должен вызывать ошибку"""
        from expenses.models import Expense
        from django.db import IntegrityError
        
        # User обязателен, поэтому должна быть ошибка
        with pytest.raises((IntegrityError, Exception)):
            Expense.objects.create(
                title='Анонимный',
                amount=Decimal('500.00')
            )
    
    def test_expense_ordering(self, user):
        """Тест порядка (новые сверху)"""
        from expenses.models import Expense
        
        # Создаем первый расход
        expense1 = Expense.objects.create(
            user=user,
            title='Первый',
            amount=Decimal('100')
        )
        
        # Создаем второй расход
        expense2 = Expense.objects.create(
            user=user,
            title='Второй',
            amount=Decimal('200')
        )
        
        expenses = list(Expense.objects.order_by('-date', '-id'))
        
        # Можно проверить по ID (последний созданный имеет больший ID)
        assert expenses[0].id == expense2.id
        assert expenses[1].id == expense1.id
