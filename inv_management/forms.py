from django import forms
from .models import Category, InventoryItem, StockTransaction

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'category', 'quantity', 'unit_price', 'description']
        widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}),
                'category': forms.Select(attrs={'class': 'form-select'}),
                'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
                'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'step':0.01}),
                'description': forms.Textarea(attrs={'class': 'form-control'}),
                'low_stock_threshold': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
      }

class StockTransactionForm(forms.ModelForm):
    class Meta:
        model = StockTransaction
        fields = ['item', 'transaction_type', 'quantity', 'notes']
        widgets = {
           'item': forms.Select(attrs={'class': 'form-select'}),
           'transaction_type': forms.Select(attrs={'class': 'form-select'}),
           'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min':0}),
           'notes': forms.Textarea(attrs={'class': 'form-control'})
        }