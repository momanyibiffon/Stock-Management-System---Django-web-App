from django.contrib import admin
from .models import Product, Client, Category, Supplier, ReceiveProduct, SaleProduct, BottleVolume


class ProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ('product_name', 'category', 'bottle_capacity', 'price_per_crate', 'quantity_in_stock',
                    'reorder_level', 'active', 'published')
    exclude = ['added_by', ]


class ClientAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ('client_name', 'mobile_number', 'email_address', 'location', 'reg_date')
    exclude = ['added_by', ]


class CategoryAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ('category_name', 'published')
    exclude = ['added_by', ]


class SupplierAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ('supplier_name', 'mobile_number', 'email_address', 'published', 'added_by')
    exclude = ['added_by', ]


class ReceiveProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.total_price = obj.quantity * obj.price_per_crate
        super().save_model(request, obj, form, change)

    list_display = ('quantity', 'supplier', 'r_price_per_crate', 'total_price', 'published')
    readonly_fields = ('total_price', 'published')
    exclude = ['added_by', ]


class SaleProductAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        obj.total_price = obj.quantity * obj.price_per_crate
        super().save_model(request, obj, form, change)

    list_display = ('quantity', 'client', 'price_per_crate', 'sale_total_price', 'published')
    readonly_fields = ('sale_total_price', 'published')
    exclude = ['added_by', ]


class BottleVolumeAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.added_by = request.user
        super().save_model(request, obj, form, change)

    list_display = ('bottle_capacity', 'published')
    exclude = ['added_by', ]


admin.site.register(Product, ProductAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ReceiveProduct, ReceiveProductAdmin)
admin.site.register(SaleProduct, SaleProductAdmin)
admin.site.register(BottleVolume, BottleVolumeAdmin)
