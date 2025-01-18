from django.urls import path
from . import views

app_name = 'inv_management'  # Add app_name for namespacing

urlpatterns = [
    # ... other urls ...
    path('', views.inventory_list, name='inventory_list'),
    path('add/', views.add_inventory_item, name='add_inventory_item'),
    path('edit/<int:item_id>/', views.edit_inventory_item, name='edit_inventory_item'),
    path('delete/<int:item_id>/', views.delete_inventory_item, name='delete_inventory_item'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add_stock_entry/<int:item_id>/', views.add_stock_entry, name='entry'),
    path('add_stock_outing/<int:item_id>/', views.add_stock_outing, name='outing'),
]