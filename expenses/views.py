# expenses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.db.models import Sum, Count
from datetime import date
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def logout_view(request):
    """Выход из системы"""
    logout(request)
    return redirect('home')

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
    expenses = Expense.objects.all().order_by('-date')[:10]

    # Статистика
    total_amount = Expense.objects.aggregate(total=Sum('amount'))['total'] or 0
    today = date.today()
    today_amount = Expense.objects.filter(date=today).aggregate(total=Sum('amount'))['total'] or 0
    total_count = Expense.objects.count()

    context = {
        'expenses': expenses,
        'total_amount': total_amount,
        'today_amount': today_amount,
        'total_count': total_count,
    }
    return render(request, 'expense_list.html', context)  # ИСПРАВЛЕНО!

@login_required
def expense_create(request):
    """Создание нового расхода"""
    if request.method == 'POST':
        title = request.POST.get('title')
        amount = request.POST.get('amount')
        
        if title and amount:
            Expense.objects.create(
                title=title,
                amount=amount,
                user=request.user
            )
            messages.success(request, 'Расход успешно добавлен!')
            return redirect('expense-list')
        else:
            messages.error(request, 'Заполните все поля!')
    
    return render(request, 'expense_form.html', {})  # ИСПРАВЛЕНО!

def expense_detail(request, pk):
    """Детали расхода"""
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expense_detail.html', {'expense': expense})  # ИСПРАВЛЕНО!

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
        expense.amount = request.POST.get('amount')
        expense.save()
        messages.success(request, 'Расход успешно обновлен!')
        return redirect('expense-detail', pk=pk)
    
    return render(request, 'expense_form.html', {'expense': expense})  # ИСПРАВЛЕНО!

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
    
    return render(request, 'expense_confirm_delete.html', {'expense': expense})  # ИСПРАВЛЕНО!

# Заглушки
def expense_chart_data(request):
    return render(request, 'expenses/chart_data.html', {})

def category_list(request):
    return render(request, 'expenses/category_list.html', {})

def budget_list(request):
    return render(request, 'expenses/budget_list.html', {})