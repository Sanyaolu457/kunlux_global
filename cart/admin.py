from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'get_total_display')
    inlines = [CartItemInline]

    def get_total_display(self, obj):
        return f"₦{obj.get_total():,.2f}"
    get_total_display.short_description = "Total"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'payment_method', 'total_price', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'payment_method', 'created_at')
    search_fields = ('user__username', 'full_name', 'phone')
    inlines = [OrderItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'get_subtotal_display')

    def get_subtotal_display(self, obj):
        return f"₦{obj.get_subtotal():,.2f}"
    get_subtotal_display.short_description = "Subtotal"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'subtotal')
