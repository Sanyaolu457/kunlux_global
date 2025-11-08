from django.shortcuts import render
from product.models import Product

def home(request):
    products = Product.objects.all().order_by('-id')[:4]
    return render(request, 'pages/home.html', {
        'title': 'Home',
        'products': products
        })


def newarrivals(request):
    return render(request, 'pages/newarrivals.html', {
        'title': 'New Arrivals',
        })

def about(request):
    return render(request, 'pages/about.html', {
        'title': 'About'
        })

def all_products(request):
    products = Product.objects.all(
    )
    return render(request, 'product/all_products.html', {'products': products})

def contact(request):
    return render(request, 'pages/contact.html', {'title': 'contact'})
