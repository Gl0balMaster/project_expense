import pytest
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from expenses.models import Expense
import factory
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'testuser{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Переопределяем для правильного создания пользователя с паролем"""
        password = kwargs.pop('password', 'testpass123')
        user = super()._create(model_class, *args, **kwargs)
        user.set_password(password)
        user.save()
        return user


class ExpenseFactory(DjangoModelFactory):
    class Meta:
        model = Expense
    
    title = factory.Sequence(lambda n: f'Тестовый расход {n}')
    amount = factory.Sequence(lambda n: Decimal(str((n + 1) * 100.50)))
    user = factory.SubFactory(UserFactory)


@pytest.fixture
def user(db):
    """Создает тестового пользователя"""
    return UserFactory()


@pytest.fixture
def superuser(db):
    """Создает суперпользователя"""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass123'
    )


@pytest.fixture
def expense(db, user):
    """Создает тестовый расход"""
    return ExpenseFactory(user=user)


@pytest.fixture
def multiple_expenses(db, user):
    """Создает несколько тестовых расходов"""
    return ExpenseFactory.create_batch(5, user=user)


@pytest.fixture
def client():
    """Тестовый клиент Django"""
    return Client()


@pytest.fixture
def authenticated_client(client, user):
    """Авторизованный тестовый клиент"""
    client.login(username=user.username, password='testpass123')
    return client


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """Автоматически дает доступ к БД всем тестам"""
    pass