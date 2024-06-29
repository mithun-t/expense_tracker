from django.urls import path
from . import views

urlpatterns = [
    path('expense/entry/', views.expense_entry, name='expense_entry'),
    path('expense/list/', views.expense_list, name='expense_list'),
    path('category/list/', views.category_list, name='category_list'),
    path('', views.home, name='home'),
]
