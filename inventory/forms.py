from django import forms
from .models import Product, ReceiveProduct, SaleProduct, Category, BottleVolume, Client, Supplier


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('product_name', 'category', 'bottle_capacity', 'price_per_crate', 'quantity_in_stock',
                  'reorder_level', 'active')


class ReceiveProductForm(forms.ModelForm):
    class Meta:
        model = ReceiveProduct
        fields = ('product_name', 'received_bottle_capacity', 'quantity', 'supplier', 'r_price_per_crate', 'total_price')


class SellProductForm(forms.ModelForm):
    class Meta:
        model = SaleProduct
        fields = ('product_name', 'sold_bottle_capacity', 'quantity', 'client', 'price_per_crate', 'sale_total_price')

    def clean_client(self):
        client = self.cleaned_data.get('client')
        if client == "":
            raise forms.ValidationError("Client name is missing")
        return client

    # def clean_quantity(self):
    #     quantity = self.cleaned_data.get('quantity')
    #
    #     initial_qty = Product.quantity_in_stock
    #     if int(quantity) < int(initial_qty):
    #         raise forms.ValidationError("Please confirm if this item is still in stock")
    #     return quantity


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_name',)


class AddBottleCapacityForm(forms.ModelForm):
    class Meta:
        model = BottleVolume
        fields = ('bottle_capacity',)


class AddCustomerForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('client_name', 'mobile_number', 'email_address', 'location')


class AddSupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ('supplier_name', 'mobile_number', 'email_address', 'location')

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data.get('mobile_number')
        try:
            int(mobile_number)
        except (ValueError, TypeError):
            raise forms.ValidationError('Please enter a valid phone number')
        return mobile_number

    # def clean_email_address(self):
    #     email_address = self.cleaned_data.get('email_address')
    #     if Supplier.objects.filter(email_address=email_address).exists():
    #         raise forms.ValidationError("Email already registered")
    #     return email_address

