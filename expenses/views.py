from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.db.models import Sum, Count
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json  # Добавить этот импорт!


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('login')  # Изменить на 'login'


def landing_page(request):
    """Стартовая страница с приветствием"""
    # Если пользователь уже авторизован, перенаправляем на главную
    if request.user.is_authenticated:
        return redirect('expense-list')

    return render(request, 'landing.html')

def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Автоматически входим после регистрации
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}! Аккаунт успешно создан.')
                return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def expense_list(request):
    """Главная страница со статистикой"""
    if request.user.is_authenticated:
        # Только расходы текущего пользователя
        expenses = Expense.objects.filter(user=request.user).order_by('-date')[:10]

        # Статистика ТОЛЬКО для текущего пользователя
        user_expenses = Expense.objects.filter(user=request.user)
        total_amount = user_expenses.aggregate(total=Sum('amount'))['total'] or 0

        today = date.today()
        today_amount = user_expenses.filter(date=today).aggregate(total=Sum('amount'))['total'] or 0

        # Расчет за месяц
        month_start = today.replace(day=1)
        month_amount = user_expenses.filter(date__gte=month_start).aggregate(total=Sum('amount'))['total'] or 0

        total_count = user_expenses.count()

        # Данные для круговой диаграммы по категориям
        category_data = user_expenses.values('category').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')

        # Преобразуем QuerySet в список для работы в шаблоне
        category_data = list(category_data)  # Просто преобразуем в список

        # Преобразуем данные для Chart.js
        chart_labels = []
        chart_data = []
        chart_colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
            '#9966FF', '#FF9F40', '#C9CBCF', '#FF6384'
        ]

        # Словарь для перевода категорий
        category_names = {
            'food': '🍔 Еда',
            'transport': '🚗 Транспорт',
            'entertainment': '🎬 Развлечения',
            'utilities': '🏠 Коммунальные услуги',
            'shopping': '🛍️ Покупки',
            'health': '🏥 Здоровье',
            'education': '📚 Образование',
            'other': '📦 Другое'
        }

        for item in category_data:
            category_name = category_names.get(item['category'], item['category'])
            chart_labels.append(category_name)
            chart_data.append(float(item['total']))

        # Если нет данных, показываем заглушку
        if not chart_data:
            chart_labels = ['Нет данных']
            chart_data = [1]
            chart_colors = ['#DDDDDD']

        # Преобразуем в JSON для передачи в шаблон
        chart_labels_json = json.dumps(chart_labels)
        chart_data_json = json.dumps(chart_data)
        chart_colors_json = json.dumps(chart_colors[:len(chart_labels)])

    else:
        # Для неавторизованных - пусто
        expenses = []
        total_amount = 0
        today_amount = 0
        month_amount = 0
        total_count = 0
        chart_labels_json = json.dumps([])
        chart_data_json = json.dumps([])
        chart_colors_json = json.dumps([])
        category_data = []

    context = {
        'expenses': expenses,
        'total_amount': total_amount,
        'today_amount': today_amount,
        'month_amount': month_amount,  # Добавлено
        'total_count': total_count,
        'category_data': category_data,
        'chart_labels': chart_labels_json,  # ВАЖНО: передаем JSON строки
        'chart_data': chart_data_json,
        'chart_colors': chart_colors_json,
    }
    return render(request, 'expense_list.html', context)


@login_required
def expense_create(request):
    """Создание нового расхода"""
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        category = request.POST.get('category', 'other')
        description = request.POST.get('description', '')

        if title and amount:
            Expense.objects.create(
                title=title,
                amount=float(amount),  # Конвертируем во float
                category=category,
                description=description,
                user=request.user
            )
            messages.success(request, 'Расход успешно добавлен!')
            return redirect('expense-list')
        else:
            messages.error(request, 'Заполните все обязательные поля!')

    return render(request, 'expense_form.html', {})


def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.user.is_authenticated and expense.user != request.user:
        messages.error(request, 'У вас нет доступа к этому расходу!')
        return redirect('expense-list')

    context = {
        'expense': expense,
        'category_choices': Expense.CATEGORY_CHOICES,
    }
    return render(request, 'expense_detail.html', context)


@login_required
def expense_update(request, pk):
    """Редактирование расхода"""
    expense = get_object_or_404(Expense, pk=pk)

    # Проверяем, что пользователь редактирует свой расход
    if expense.user != request.user:
        messages.error(request, 'Вы не можете редактировать чужой расход!')
        return redirect('expense-list')

    if request.method == 'POST':
        expense.title = request.POST.get('title')
        expense.amount = float(request.POST.get('amount'))
        expense.category = request.POST.get('category', 'other')
        expense.description = request.POST.get('description', '')
        expense.save()
        messages.success(request, 'Расход успешно обновлен!')
        return redirect('expense-detail', pk=pk)

    return render(request, 'expense_form.html', {'expense': expense})


@login_required
def expense_delete(request, pk):
    """Удаление расхода"""
    expense = get_object_or_404(Expense, pk=pk)

    # Проверяем, что пользователь удаляет свой расход
    if expense.user != request.user:
        messages.error(request, 'Вы не можете удалить чужой расход!')
        return redirect('expense-list')

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Расход успешно удален!')
        return redirect('expense-list')

    context = {
        'expense': expense,
        'category_choices': Expense.CATEGORY_CHOICES,
    }

    return render(request, 'expense_confirm_delete.html', context)


# Заглушки можно удалить или оставить
def expense_chart_data(request):
    return render(request, 'expenses/chart_data.html', {})


def category_list(request):
    return render(request, 'expenses/category_list.html', {})


def budget_list(request):
    return render(request, 'expenses/budget_list.html', {})