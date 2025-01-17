from django.shortcuts import render, redirect, get_object_or_404
from .models import InventoryItem, Category
from django.contrib.auth.decorators import login_required
from django.db.models import Q # type: ignore
from .forms import CategoryForm, InventoryItemForm
from django.db import IntegrityError

@login_required
def inventory_list(request):

    search_term = request.GET.get('search', '')
    
    if search_term:
         items = InventoryItem.objects.filter(
            Q(name__icontains=search_term) | Q(category__name__icontains=search_term), # Search in name and blood_type
        ) 
    else:
        items = InventoryItem.objects.all()

    context = {
        'items': items,
        'search_term': search_term
    }
    
    return render(request, 'inventory_list.html', context)

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
  return render(request, 'inventory/add_inventory_item.html', {'categories': categories, 'form': form})

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