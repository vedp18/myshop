from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from cart.forms import CartAddProductForm

# Product list view
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                   'shop/product/product_list.html', 
                   {
                       'category': category,
                       'categories': categories,
                       'products': products
                    }
                )

# Product detail view
def product_detail(request, id, product_slug=None):
    if product_slug:
        product = get_object_or_404(Product,
                                    id=id,
                                    slug=product_slug,
                                    available=True)
    else:
        product = get_object_or_404(Product, id=id, available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'shop/product/product_detail.html',
                  {
                      'product': product,
                      'cart_product_form': cart_product_form
                  })    





