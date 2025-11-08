from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from product.models import Product

@login_required(login_url='login')
def cart_detail(request):
    cart = request.session.get('cart', {})
    products = []
    total = 0

    for id, item in cart.items():
        product = get_object_or_404(Product, id=id)
        subtotal = product.price * item['quantity']
        total += subtotal
        products.append({
            'product': product,
            'quantity': item['quantity'],
            'subtotal': subtotal,
        })

    return render(request, 'cart_detail.html', {'products': products, 'total': total})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if not request.user.is_authenticated:
        request.session['redirect_after_login'] = product.id
        messages.info(request, "Please log in to add items to your cart.")
        return redirect('login')

    cart = request.session.get('cart', {})
    if str(product_id) not in cart:
        cart[str(product_id)] = {'quantity': 1}
    else:
        cart[str(product_id)]['quantity'] += 1

    request.session['cart'] = cart
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart_detail')

@login_required(login_url='login')
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_detail')
