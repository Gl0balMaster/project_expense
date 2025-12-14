# users/views.py
from django.shortcuts import render

def register_view(request):
    """Простая страница регистрации"""
    return render(request, 'users/register.html', {})