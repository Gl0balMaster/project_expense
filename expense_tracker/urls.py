from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from expenses.views import expense_list, expense_create, expense_detail, expense_update, expense_delete, register, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Аутентификация
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    
    path('logout/', logout_view, name='logout'),
    
    path('register/', register, name='register'),
    
    # Основные маршруты расходов
    # Главная страница
    path('', expense_list, name='home'),
    
    # Все расходы (альтернативный путь к главной)
    path('expenses/', expense_list, name='expense-list'),
    
    # Создание расхода
    path('expenses/create/', expense_create, name='expense-create'),
    
    # Детали, обновление, удаление расхода
    path('expenses/<int:pk>/', expense_detail, name='expense-detail'),
    path('expenses/<int:pk>/update/', expense_update, name='expense-update'),
    path('expenses/<int:pk>/delete/', expense_delete, name='expense-delete'),
]