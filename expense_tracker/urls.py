from django.contrib import admin
from django.urls import path
from expenses.views import expense_list, expense_create, expense_detail, expense_update, expense_delete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', expense_list, name='home'),
    path('expenses/', expense_list, name='expense-list'),
    path('expenses/create/', expense_create, name='expense-create'),
    path('expenses/<int:pk>/', expense_detail, name='expense-detail'),
    path('expenses/<int:pk>/update/', expense_update, name='expense-update'),
    path('expenses/<int:pk>/delete/', expense_delete, name='expense-delete'),
]
