from django.urls import path
from . import views

app_name = 'inventory'
urlpatterns = [
    path('', views.index_view, name="index"),
    path('products/', views.products_view, name="products"),
    path('products/add-product/', views.add_product_view, name="add_product"),
    path('product/<int:p_id>/product-details', views.product_details_view, name="product_details"),
    path('product/<int:p_id>/edit-product', views.update_product_view, name="edit_product"),
    path('product/<int:p_id>/receive-product', views.receive_product_view, name="receive_product"),
    path('product/<int:product_id>/sell-product', views.sell_product_view, name="sell_product"),
    path('products/out_of_stock', views.out_of_stock, name="out_of_stock"),
    path('customers/', views.customers_view, name="customers"),
    path('customer/<int:customer_id>/customer-details', views.customer_details_view, name="customer_details"),
    path('add-customer/', views.add_customer_view, name="add_customer"),
    path('customer/<int:customer_id>/edit-customer', views.update_customer_view, name="edit_customer"),
    path('categories/', views.categories_view, name="categories"),
    path('new-categories/', views.create_categories_view, name="new_categories"),
    path('categories/<int:category_id>/edit-category', views.update_category_view, name="edit_category"),
    path('bottle-capacity/', views.bottle_capacity_view, name="bottle_capacity"),
    path('bottle-capacity/new/', views.create_bottle_capacity_view, name="add_bottle_capacity"),
    path('bottle-capacity/<int:bottle_id>/edit', views.update_bottle_capacity_view, name="edit_bottle_capacity"),
    path('suppliers/', views.suppliers_view, name="suppliers"),
    path('add-supplier/', views.add_supplier_view, name="add_supplier"),
    path('supplier/<int:supplier_id>/supplier-details', views.supplier_details_view, name="supplier_details"),
    path('supplier/<int:supplier_id>/edit-supplier', views.update_supplier_view, name="edit_supplier"),
    path('export_csv', views.all_products_export_csv, name="export-csv"),
    path('products/received-products/', views.purchased_products, name='purchased_products'),
    path('products/received-products/<int:product_id>/edit-received-product', views.update_received_product_view,
         name='update_received_product'),
    path('products/sold-products/', views.sold_products, name='sold_products'),
    path('products/sold-products/<int:product_id>', views.update_sold_product_view, name='update_sale'),

    # delete urls
    path('delete-product/<int:prod_id>', views.delete_product, name='delete_product'),
    path('delete-category/<int:cat_id>', views.delete_category, name='delete_category'),
    path('delete-capacity/<int:cap_id>', views.delete_bottle_capacity, name='delete_capacity'),
    path('delete-supplier/<int:supl_id>', views.delete_supplier, name='delete_supplier'),
    path('delete-customer/<int:cust_id>', views.delete_customer, name='delete_customer'),
]
