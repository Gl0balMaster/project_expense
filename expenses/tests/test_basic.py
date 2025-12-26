import pytest
from decimal import Decimal


@pytest.mark.django_db
def test_basic_assertion():
    assert 1 + 1 == 2


@pytest.mark.django_db
def test_expense_model():
    """Тест создания модели Expense"""
    from expenses.models import Expense
    from django.contrib.auth.models import User
    
    user = User.objects.create_user(
        username='testuser',
        password='testpass123'
    )
    
    expense = Expense.objects.create(
        user=user,
        title='Тестовый расход',
        amount=Decimal('1500.50')
    )
    
    assert expense.title == 'Тестовый расход'
    assert expense.amount == Decimal('1500.50')
    assert str(expense) == 'Тестовый расход - 1500.50 Br'