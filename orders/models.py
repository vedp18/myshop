from django.db import models
from shop.models import Product

# Order model to represent customer orders
class Order(models.Model):
    """Model to represent an order placed by a customer."""

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        """String representation of the Order model."""
        return f'Order {self.id} by {self.first_name} {self.last_name}'
        
    def get_total_cost(self):
        """Calculate the total cost of the order."""
        return sum(item.get_cost() for item in self.items.all())
        

# OrderItem model to represent items in an order
class OrderItem(models.Model):
    """Model to represent an item in an order."""

    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, 
                                related_name='order_items',
                                on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        """String representation of the OrderItem model."""
        return f'{self.quantity} x {self.product.name} (Order {self.order.id})'
    
    def get_cost(self):
        """Calculate the cost of the order item."""
        return self.price * self.quantity
    
