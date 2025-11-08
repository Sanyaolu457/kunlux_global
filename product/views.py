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
