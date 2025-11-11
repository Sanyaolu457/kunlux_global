from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list(request):
    products = Product.objects.all().order_by('-id')
    return render(request, 'product/products.html', {
        'title': 'New Arrivals',
        'products': products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_detail.html', {
        'title': product.name,
        'product': product
    })


from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list_cate(request):
    products = Product.objects.all().order_by('-id')
    categories = Category.objects.all()
    return render(request, 'product/productsCat.html', {
        'title': 'All Products',
        'products': products,
        'categories': categories
    })


def products_by_category(request, category_slug):
    """Show products filtered by category slug."""
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(custom_category=category).order_by('-id')
    categories = Category.objects.all()

    return render(request, 'product/products_by_category.html', {
        'title': f"{category.name} Products",
        'category': category,
        'products': products,
        'categories': categories
    })
