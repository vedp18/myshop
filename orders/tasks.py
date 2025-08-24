from celery import shared_task
from django.core.mail import send_mail
from .models import Order

# Task to send order confirmation email
@shared_task
def send_order_confirmation_email(order_id):
    """Send an order confirmation email."""
    order = Order.objects.get(id=order_id)
    subject = f"Order Confirmation #{order.id}"
    message = f"Dear {order.first_name}, \n\n" \
                f"You have successfully placed an order. \n" \
                f"Order ID: {order.id}\n" \
                f"Thank you for your order!\n\n"
    mail_sent = send_mail( subject=subject,
                            message=message,
                            from_email='MyShop <no-reply@myshop.com>',
                            recipient_list=[order.email])
    return mail_sent
