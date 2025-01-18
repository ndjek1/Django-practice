from django.shortcuts import render, redirect, get_object_or_404
from .models import InventoryItem, Category, StockTransaction
from django.contrib.auth.decorators import login_required
from django.db.models import Q # type: ignore
from .forms import CategoryForm, InventoryItemForm, StockTransactionForm
from django.db import IntegrityError

@login_required
def inventory_list(request):
    search_term = request.GET.get('search', '')
    filter_type = request.GET.get('filter', 'all')

    if search_term:
         items = InventoryItem.objects.filter(
            Q(name__icontains=search_term) | Q(category__name__icontains=search_term)
        )
    elif filter_type == 'out_of_stock':
        items = InventoryItem.objects.filter(quantity__lte=0)
    elif filter_type == 'low_stock':
        items = InventoryItem.objects.filter(quantity__lte=models.F('low_stock_threshold')).filter(quantity__gt=0)
    else:
       items = InventoryItem.objects.all()

    return render(request, 'inventory_list.html', {'items': items, 'search_term': search_term, 'filter_type': filter_type})

@login_required
def add_inventory_item(request):
  if request.method == 'POST':
      form = InventoryItemForm(request.POST)
      if form.is_valid():
           form.save()
           return redirect('inv_management:inventory_list')

  else:
     form = InventoryItemForm()

  categories = Category.objects.all()
  return render(request, 'add_inventory_item.html', {'categories': categories, 'form': form})

@login_required
def edit_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item) # Bind the form to the model object
        if form.is_valid():
            form.save()
            return redirect('inv_management:inventory_list')
    else:
      form = InventoryItemForm(instance=item) # Create a new form bound to the model instance
    categories = Category.objects.all()
    return render(request, 'edit_inventory_item.html', {'item': item, 'categories': categories, 'form': form})


@login_required
def delete_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    item.delete()
    return redirect('inv_management:inventory_list')


# Category views
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST) # Get form from request.POST
        if form.is_valid(): # Validate the form data
            try:
                form.save() # Save the form in the database
                return redirect('inv_management:category_list')
            except IntegrityError:
                form.add_error('name', 'A category with this name already exists.') # add error to the name field
        # If the form is not valid, it will be rendered with the errors
    else:
        form = CategoryForm() # Create a new empty form

    return render(request, 'add_category.html', {'form': form})


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
      category.name = request.POST['name']
      category.save()
      return redirect('inv_management:category_list')
    return render(request, 'edit_category.html', {'category': category})


@login_required
def delete_category(request, category_id):
  category = get_object_or_404(Category, pk=category_id)
  category.delete()
  return redirect('inv_management:category_list')


@login_required
def add_stock_entry(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        quantity = request.POST['quantity']  # Use bracket notation to get the value
        notes = request.POST.get('notes', '')  # Use .get() to handle optional fields safely
        
        # Create the transaction object manually
        transaction = StockTransaction(
            item=item,  # Pass the actual item object
            quantity=quantity,
            notes=notes,
            transaction_type='entry',  # Set the transaction type
        )
        transaction.save()

        # Update the inventory item's quantity
        item.quantity += int(quantity)
        item.save()

        return redirect('inv_management:inventory_list')
    else:
        print('Form not valid')
        form = StockTransactionForm()
    return render(request, 'add_stock_transaction.html', {'item': item, 'form': form, 'type': 'entry'})


@login_required
def add_stock_outing(request, item_id):
    item = get_object_or_404(InventoryItem, pk=item_id)
    if request.method == 'POST':
        form = StockTransactionForm(request.POST)
        quantity = int(request.POST['quantity'])  # Convert to integer
        notes = request.POST.get('notes', '')  # Optional notes field
    
        transaction = StockTransaction(
            item=item,  # Pass the actual item object
            quantity=quantity,  # Use the converted integer
            notes=notes,
            transaction_type='outing',  # Set the correct transaction type
        )
        
        # Validate stock quantity
        if item.quantity < transaction.quantity:
            form.add_error('quantity', 'The outing quantity exceeds the current stock.')
        else:
            # Save the transaction
            transaction.save()

            # Update the inventory item's quantity
            item.quantity -= quantity
            item.save()
            
            return redirect('inv_management:inventory_list')
    else:
        form = StockTransactionForm()
    
    return render(request, 'add_stock_transaction.html', {'item': item, 'form': form, 'type': 'outing'})
