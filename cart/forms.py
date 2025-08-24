from django import forms
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 41)]

class CartAddProductForm(forms.Form):
    """Form for adding a product to the cart."""
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,)
    # quantity = forms.IntegerField(min_value=1, max_value=20,)
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
