from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import send_order_confirmation_email

def order_create(request):
    """Create a new order."""
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Clear the cart after order creation
            cart.clear()
            # Send order confirmation email
            send_order_confirmation_email.delay(order.id)
        return render(request, 'orders/order/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/order_create.html', {'cart': cart, 'form': form})
