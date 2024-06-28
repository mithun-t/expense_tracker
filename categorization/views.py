# categorization/views.py

from django.shortcuts import render, redirect
from django.db.models import Sum
from decimal import Decimal
from .models import Expense, Category, SubCategory
from .forms import ExpenseForm

def expense_entry(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expense_list')  # Redirect to expense list view after saving
    else:
        form = ExpenseForm()
    
    return render(request, 'categorization/expense_entry.html', {'form': form})

def expense_list(request):
    category_filter = request.GET.get('category')
    subcategory_filter = request.GET.get('subcategory')

    expenses = Expense.objects.all().order_by('date')
    if category_filter:
        expenses = expenses.filter(category_id=category_filter)
    if subcategory_filter:
        expenses = expenses.filter(subcategory_id=subcategory_filter)

    # Aggregating totals
    category_totals = Expense.objects.values('category__name').annotate(total_amount=Sum('amount'))
    subcategory_totals = Expense.objects.values('subcategory__name').annotate(total_amount=Sum('amount'))

    # Convert Decimal to float for JSON serialization
    subcategory_totals = [{'subcategory__name': total['subcategory__name'], 'total_amount': float(total['total_amount'])} for total in subcategory_totals]

    # Calculate grand totals
    grand_total_expenses = float(expenses.aggregate(grand_total=Sum('amount'))['grand_total'] or 0)
    grand_total_category = float(category_totals.aggregate(grand_total=Sum('total_amount'))['grand_total'] or 0)
    grand_total_subcategory = float(sum(total['total_amount'] for total in subcategory_totals))

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    # Data for Chart.js
    subcategory_names = [total['subcategory__name'] for total in subcategory_totals]
    subcategory_amounts = [total['total_amount'] for total in subcategory_totals]

    return render(request, 'categorization/expense_list.html', {
        'expenses': expenses,
        'category_totals': category_totals,
        'subcategory_totals': subcategory_totals,
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': category_filter,
        'selected_subcategory': subcategory_filter,
        'grand_total_expenses': grand_total_expenses,
        'grand_total_category': grand_total_category,
        'grand_total_subcategory': grand_total_subcategory,
        'subcategory_names': subcategory_names,
        'subcategory_amounts': subcategory_amounts,
    })
