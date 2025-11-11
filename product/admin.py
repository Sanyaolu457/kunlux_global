from django.contrib import admin
from .models import Product, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'custom_category')
    list_filter = ('category', 'custom_category', 'tags')
    search_fields = ('name', 'description')
    filter_horizontal = ('tags',)
