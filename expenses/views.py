from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from django.db.models import Sum, Count
from datetime import date

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
    return render(request, 'expenses/expense_list.html', context)

def expense_create(request):
    """Создание нового расхода"""
    if request.method == 'POST':
        # Здесь будет логика сохранения
        return redirect('expense-list')
    return render(request, 'expenses/expense_form.html', {})

def expense_detail(request, pk):
    """Детали расхода"""
    expense = get_object_or_404(Expense, pk=pk)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})

def expense_update(request, pk):
    """Редактирование расхода"""
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        # Здесь будет логика обновления
        return redirect('expense-detail', pk=pk)
    return render(request, 'expenses/expense_form.html', {'expense': expense})

def expense_delete(request, pk):
    """Удаление расхода"""
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('expense-list')
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})
