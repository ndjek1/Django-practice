from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    
    def __str__(self):
      return self.name
    
    def is_out_of_stock(self):
         return self.quantity <= 0
    def is_low_stock(self):
        return self.quantity <= self.low_stock_threshold
    
    def __str__(self):
      return self.name
    


class StockTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('entry', 'Entry'),
        ('outing', 'Outing'),
    ]
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    transaction_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
      return f"{self.get_transaction_type_display()} - {self.item.name} - {self.quantity}"