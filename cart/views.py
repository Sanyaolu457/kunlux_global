from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from product.models import Product
from .models import Cart, CartItem


@login_required(login_url='login')
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')
    total = cart.get_total()
    return render(request, 'cart_detail.html', {'cart': cart, 'cart_items': cart_items, 'total': total})


@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"{product.name} added to your cart.")
    return redirect('cart_detail')


@login_required(login_url='login')
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
    if cart_item:
        cart_item.delete()
    messages.info(request, "Item removed from your cart.")
    return redirect('cart_detail')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem

@login_required(login_url='login')
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart_detail')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        payment_method = request.POST.get('payment_method')

        if not all([full_name, address, phone, payment_method]):
            messages.error(request, "Please fill all required fields.")
            return redirect('checkout')

        # Calculate total
        total = cart.get_total()

        # Create Order
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            payment_method=payment_method,
            total_price=total,
            is_paid=True if payment_method in ['card', 'transfer'] else False
        )

        # Create Order Items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                subtotal=item.get_subtotal(),
            )

        # Clear Cart
        cart.items.all().delete()

        messages.success(request, f"Checkout successful! Your order total is ₦{total}")
        return redirect('my_orders')

    cart_items = cart.items.all()
    total = cart.get_total()

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order

@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    if not orders.exists():
        messages.info(request, "You have no orders yet.")
    
    return render(request, 'my_orders.html', {'orders': orders})
