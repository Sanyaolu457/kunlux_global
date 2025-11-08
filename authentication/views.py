from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from product.models import Product
from .forms import CustomUserRegistrationForm, CustomLoginForm


def register(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('pages_home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')

                pending_cart_item = request.session.pop('pending_cart_item', None)
                if pending_cart_item:
                    product = get_object_or_404(Product, id=pending_cart_item)
                    cart = request.session.get('cart', {})
                    cart[str(pending_cart_item)] = {'quantity': 1}
                    request.session['cart'] = cart
                    messages.success(request, f"{product.name} added to your cart.")

                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect('pages_home')

        messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


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
        messages.info(request, "Please log in to add items to your cart.")
        request.session['pending_cart_item'] = product_id
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

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
        messages.warning(request, "Item removed from cart.")
    return redirect('cart_detail')
