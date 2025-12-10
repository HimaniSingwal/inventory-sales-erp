from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    change = models.IntegerField()   # +10 = stock in, -5 = stock out
    reason = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} ({self.change})"


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sale of {self.product.name} x {self.quantity}"



