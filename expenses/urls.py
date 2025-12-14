from django.urls import path
from . import views

urlpatterns = [
    path('', views.expense_list, name='expense-list'),
    path('create/', views.expense_create, name='expense-create'),
    path('<int:pk>/', views.expense_detail, name='expense-detail'),
    path('<int:pk>/update/', views.expense_update, name='expense-update'),
    path('<int:pk>/delete/', views.expense_delete, name='expense-delete'),
    path('chart-data/', views.expense_chart_data, name='expense-chart-data'),
    path('categories/', views.category_list, name='category-list'),
    path('budgets/', views.budget_list, name='budget-list'),
]