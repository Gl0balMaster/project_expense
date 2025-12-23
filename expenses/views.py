from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.db.models import Sum, Count
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('login')


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register/register.html', {'form': form})


def expense_list(request):
    """Главная страница со статистикой - ТОЛЬКО ДЛЯ ТЕКУЩЕГО ПОЛЬЗОВАТЕЛЯ!"""
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
    else:
        # Для неавторизованных - пусто
        expenses = []
        total_amount = 0
        today_amount = 0
        month_amount = 0
        total_count = 0

    context = {
        'expenses': expenses,
        'total_amount': total_amount,
        'today_amount': today_amount,
        'month_amount': month_amount,
        'total_count': total_count,
    }
    return render(request, 'expense_list.html', context)


@login_required
def expense_create(request):
    """Создание нового расхода"""
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')

        if title and amount:
            Expense.objects.create(
                title=title,
                amount=float(amount),  # Конвертируем во float
                user=request.user  # Привязываем к пользователю
            )
            messages.success(request, 'Расход успешно добавлен!')
            return redirect('expense-list')
        else:
            messages.error(request, 'Заполните все поля!')

    return render(request, 'expense_form.html', {})


def expense_detail(request, pk):
    """Детали расхода"""
    expense = get_object_or_404(Expense, pk=pk)

    # ПРОВЕРКА: пользователь может смотреть только СВОИ расходы
    if request.user.is_authenticated and expense.user != request.user:
        messages.error(request, 'У вас нет доступа к этому расходу!')
        return redirect('expense-list')

    return render(request, 'expense_detail.html', {'expense': expense})


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
        expense.amount = float(request.POST.get('amount'))  # Конвертируем
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

    return render(request, 'expense_confirm_delete.html', {'expense': expense})