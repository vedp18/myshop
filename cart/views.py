from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import CartAddProductForm
from .cart import Cart
from shop.models import Product

@require_POST
def cart_add(request, product_id):
    """Add a product to the cart."""
    # Initialize the cart
    cart = Cart(request)
    # Get the product by ID
    product = get_object_or_404(Product, id=product_id)
    # Create the form instance with POST data
    form = CartAddProductForm(request.POST)
    # Check if the form is valid
    if form.is_valid():
        # Extract the cleaned data from the form
        cd = form.cleaned_data
        # Add the product to the cart
        cart.add(product=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['override'])

    # Redirect to the cart view
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove a product from the cart."""

    # Initialize the cart
    cart = Cart(request)
    # Get the product by ID
    product = get_object_or_404(Product, id=product_id)
    # Remove the product from the cart
    cart.remove(product)

    # Redirect to the cart view
    return redirect('cart:cart_detail')


def cart_detail(request):
    """Display the cart details."""

    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True})

    return render(request, 'cart/cart_detail.html', {'cart': cart})
