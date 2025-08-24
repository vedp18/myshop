from django.db import models
from django.urls import reverse


# Category model
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # return f"/shop/category/{self.slug}/" OR
        return reverse('shop:product_list_by_category', args=[self.slug])


    
# Product model
class Product(models.Model):
    # Product details
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    # Price and stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ['name']
        indexes = [
            # ID and slug for quick lookups
            models.Index(fields=['id', 'slug']),
            # Name for search functionality
            models.Index(fields=['name']),
            # Created at for sorting
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        # return f"/shop/product/{self.id}/{self.slug}/"  OR
        return reverse('shop:product_detail', args=[self.id, self.slug])
    

