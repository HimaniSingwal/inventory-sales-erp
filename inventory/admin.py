from django.contrib import admin
from .models import Product, StockMovement, Sale


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "quantity")
    search_fields = ("name", "sku")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("product", "change", "reason", "created_at")
    list_filter = ("product", "created_at")


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "price_at_sale", "created_at")
    list_filter = ("product", "created_at")
    search_fields = ("product__name", "product__sku")


