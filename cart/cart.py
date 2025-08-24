from decimal import Decimal
from django.conf import settings
from shop.models import Product

class Cart:
    def __init__(self, request):
        """Initialize the cart with the session data.

        :param request: The HTTP request object.
        """

        self.session = request.session
        cart = self.session.get(settings.SESSION_CART_ID)
        if not cart:
            cart = self.session[settings.SESSION_CART_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Add a product to the cart or update its quantity.

        :param product: The product to add.
        :param quantity: The quantity of the product to add.
        :param override_quantity: If True, override the existing quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Save the cart to the session."""
        self.session[settings.SESSION_CART_ID] = self.cart
        # Mark the session as modified to ensure it is saved
        # even if no other data has changed.
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart.
        :param product: The product to remove.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        """Iterate over the items in the cart and yield each product."""
        product_ids = self.cart.keys()
        # Get the products from the database
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        # Add the product details to the cart items
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Return the total number of items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """Return the total price of all items in the cart."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self):
        """Clear the cart."""
        del self.session[settings.SESSION_CART_ID]
        self.session.modified = True
        self.cart = {}