from django.contrib import admin
from .models import Item, Order, Discount, Tax, BasketItem
from django.contrib.sessions.models import Session


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price']
    list_filter = ['name', 'description', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'discount']
    list_filter = ['id', 'discount']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'discount', 'discount_id']
    list_filter = ['name', 'discount', 'discount_id']


class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'tax', 'tax_id']
    list_filter = ['name', 'tax', 'tax_id']


class BasketItemAdmin(admin.ModelAdmin):
    list_display = ['item', 'quantity', 'order']
    list_filter = ['item', 'quantity', 'order']


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(BasketItem, BasketItemAdmin)
admin.site.register(Session)
