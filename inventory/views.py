from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import ReceiveProductForm, SellProductForm, AddCategoryForm, AddBottleCapacityForm, AddCustomerForm, \
    AddSupplierForm, ProductForm
from django.contrib import messages
from .filters import ProductFilter
from accounts.decorators import allowed_users
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import csv
import datetime


@login_required
def index_view(request):
    template = 'inventory/index.html'
    title = 'Stock Management System'
    sl = Product.objects.all()
    sls = Product.reorder_level
    products_out_of_stock = Product.objects.filter(quantity_in_stock__lte=50).count()
    total_sales = SaleProduct.objects.all().count()
    total_purchases = ReceiveProduct.objects.all().count()
    latest_sales = SaleProduct.objects.all().order_by('-published')[:3]
    latest_purchases = ReceiveProduct.objects.all().order_by('-published')[:3]

    context = {
        'title': title,
        'products_out_of_stock': products_out_of_stock,
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'latest_sales': latest_sales,
        'latest_purchases': latest_purchases,
    }
    return render(request, template, context)


@login_required
def out_of_stock(request):
    template = 'inventory/out_of_stock.html'
    title = 'Out of stock'
    products_out_of_stock = Product.objects.filter(quantity_in_stock__lte=50)

    context = {
        'title': title,
        'products_out_of_stock': products_out_of_stock,
    }
    return render(request, template, context)


@login_required
def products_view(request):
    template = 'inventory/products.html'
    title = 'In stock'

    all_products = Product.objects.filter(active=True).order_by('-published')
    products_count = all_products.count()
    product_filter = ProductFilter(request.GET, queryset=all_products)
    all_products = product_filter.qs

    context = {
        'title': title,
        'all_products': all_products,
        'product_filter': product_filter,
        'products_count': products_count,
    }
    return render(request, template, context)


@login_required
def product_details_view(request, p_id):
    template = 'inventory/product_details.html'
    title = 'Manage product'
    product = Product.objects.get(id=p_id)

    context = {
        'title': title,
        'product': product,
    }
    return render(request, template, context)


@login_required
def add_product_view(request):
    template = 'inventory/add_product.html'
    title = 'New product'

    all_products = Product.objects.filter(active=True)

    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "New product added successfully")
            return redirect('../')
    else:
        product_form = ProductForm()

    context = {
        'title': title,
        'all_products': all_products,
        'product_form': product_form,
    }
    return render(request, template, context)


@login_required
def update_product_view(request, p_id):
    template = 'inventory/add_product.html'
    title = 'Update product'

    all_products = Product.objects.filter(active=True)
    product = get_object_or_404(Product, id=p_id)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Product updated successfully")
            return redirect('./product-details')
    else:
        product_form = ProductForm(instance=product)

    context = {
        'title': title,
        'all_products': all_products,
        'product_form': product_form,
    }
    return render(request, template, context)

@login_required
def receive_product_view(request, p_id):
    template = 'inventory/receive_product.html'
    title = 'Receive product'
    # all_products = Product.objects.get(id=p_id)
    all_products = get_object_or_404(Product, id=p_id)

    initial_data = {
        "product_name": all_products.product_name,
        "received_bottle_capacity": all_products.bottle_capacity,
        "r_price_per_crate": all_products.price_per_crate
    }

    if request.method == 'POST':
        form = ReceiveProductForm(request.POST)
        form2 = ReceiveProductForm(request.POST, instance=all_products)
        if form.is_valid():
            prod = form.save(commit=False)
            qty = request.POST.get('quantity')
            all_products.quantity_in_stock += int(qty)
            form2.save()
            prod.save()
            messages.success(request, "Product received successfully")

            return redirect('./product-details')

    else:
        form = ReceiveProductForm(initial=initial_data)
    context = {
        'title': title,
        'product': all_products,
        'form': form,
    }
    return render(request, template, context)


@login_required
def sell_product_view(request, product_id):
    # prod_details = Product.objects.get(id=product_id)

    template = 'inventory/issue_product.html'
    title = 'Issue product'

    product = get_object_or_404(Product, id=product_id)
    # product = Product.objects.get(id=product_id)

    initial_data = {
        "product_name": product.product_name,
        "sold_bottle_capacity": product.bottle_capacity,
        "price_per_crate": product.price_per_crate
    }

    if request.method == "POST":
        form = SellProductForm(request.POST)
        form2 = SellProductForm(request.POST, instance=product)
        if form.is_valid():
            instance = form.save(commit=False)
            quantity = request.POST.get("quantity")
            if int(quantity) <= product.quantity_in_stock:
                product.quantity_in_stock -= int(quantity)
                form2.save()
                instance.save()
                messages.success(request, "Product sold successfully")
                return redirect('./product-details')
            else:
                messages.error(request, "This product might be out of stock")
    else:
        form = SellProductForm(initial=initial_data)

    context = {
        'title': title,
        'product': product,
        'form': form,
    }
    return render(request, template, context)


@login_required
def delete_product(request, prod_id):
    prod = get_object_or_404(Product, id=prod_id)
    prod.delete()
    messages.success(request, "Product successfully deleted")
    return redirect('/products')


@login_required
def categories_view(request):
    template = 'inventory/categories.html'
    title = 'Product Categories'

    all_categories = Category.objects.all()

    # this form creates a new category
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully")
    else:
        form = AddCategoryForm()
    context = {
        'title': title,
        'all_categories': all_categories,
        'form': form,
    }
    return render(request, template, context)


@login_required
def create_categories_view(request, c_id):
    template = 'inventory/categories.html'
    title = 'Add New Category'

    all_categories = Category.objects.get()

    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully")
    else:
        form = AddCategoryForm()
    context = {
        'title': title,
        'all_categories': all_categories,
    }
    return render(request, template, context)


@login_required
def update_category_view(request, category_id):
    template = 'inventory/add_category.html'
    title = 'Edit Category'

    category = get_object_or_404(Category, id=category_id)
    # this form updates the product categories
    if request.method == 'POST':
        category_form = AddCategoryForm(request.POST, instance=category)
        if category_form.is_valid():
            form = category_form.save(commit=False)
            form.save()
            messages.success(request, "Category updated successfully")
            return redirect('../../categories')
    else:
        category_form = AddCategoryForm(instance=category)
    context = {
        'title': title,
        'category': category,
        'category_form': category_form,
    }
    return render(request, template, context)


@login_required
def delete_category(request, cat_id):
    category = get_object_or_404(Category, id=cat_id)
    category.delete()
    messages.success(request, "Product category has been successfully deleted")
    return redirect('/categories')


@login_required
def create_bottle_capacity_view(request):
    template = 'inventory/add_bottle_capacity.html'
    title = 'New bottle Volume'

    all_bottles = BottleVolume.objects.all()
    # this form creates a new bottle capacity
    if request.method == 'POST':
        form = AddBottleCapacityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New bottle capacity added successfully")
            return redirect('../')
    else:
        form = AddBottleCapacityForm()
    context = {
        'title': title,
        'all_bottles': all_bottles,
        'form': form,
    }
    return render(request, template, context)


@login_required
def update_bottle_capacity_view(request, bottle_id):
    template = 'inventory/add_bottle_capacity.html'
    title = 'Update Bottle Volume'

    bottle_volume = get_object_or_404(BottleVolume, id=bottle_id)
    # this form updates the product bottle volumes
    if request.method == 'POST':
        bottle_volume_form = AddBottleCapacityForm(request.POST, instance=bottle_volume)
        if bottle_volume_form.is_valid():
            form = bottle_volume_form.save(commit=False)
            form.save()
            messages.success(request, "Bottle volume updated successfully")
            return redirect('../')
    else:
        bottle_volume_form = AddBottleCapacityForm(instance=bottle_volume)
    context = {
        'title': title,
        'bottle_volume': bottle_volume,
        'form': bottle_volume_form,
    }
    return render(request, template, context)


@login_required
def bottle_capacity_view(request):
    template = 'inventory/bottle_capacity.html'
    title = 'Bottle Volumes'

    all_bottles = BottleVolume.objects.all()
    # this form creates a new bottle capacity
    if request.method == 'POST':
        form = AddBottleCapacityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New bottle capacity added successfully")
    else:
        form = AddBottleCapacityForm()
    context = {
        'title': title,
        'all_bottles': all_bottles,
        'form': form,
    }
    return render(request, template, context)


@login_required
def delete_bottle_capacity(request, cap_id):
    capacity = get_object_or_404(BottleVolume, id=cap_id)
    capacity.delete()
    messages.success(request, "Bottle volume has been successfully deleted")
    return redirect('/bottle-capacity')


@login_required
def suppliers_view(request):
    template = 'inventory/suppliers.html'
    title = 'Suppliers'

    all_suppliers = Supplier.objects.all()
    # this form adds a new customer
    if request.method == 'POST':
        supplier_form = AddSupplierForm(request.POST)
        if supplier_form.is_valid():
            supplier_form.save()
            messages.success(request, "New supplier added successfully")
    else:
        supplier_form = AddSupplierForm()
    context = {
        'title': title,
        'all_suppliers': all_suppliers,
        'supplier_form': supplier_form,
    }
    return render(request, template, context)


@login_required
def supplier_details_view(request, supplier_id):
    template = 'inventory/supplier_details.html'
    title = 'Supplier Details'

    supplier_details = Supplier.objects.get(id=supplier_id)
    context = {
        'title': title,
        'supplier_details': supplier_details,
    }
    return render(request, template, context)


@login_required
def add_supplier_view(request):
    template = 'inventory/add_supplier.html'
    title = 'Add Supplier'

    all_suppliers = Supplier.objects.all()
    # this form adds a new customer
    if request.method == 'POST':
        supplier_form = AddSupplierForm(request.POST)
        if supplier_form.is_valid():
            supplier_form.save()
            messages.success(request, "New supplier added successfully")
            return redirect('/suppliers')
    else:
        supplier_form = AddSupplierForm()
    context = {
        'title': title,
        'all_suppliers': all_suppliers,
        'supplier_form': supplier_form,
    }
    return render(request, template, context)


@login_required
def update_supplier_view(request, supplier_id):
    template = 'inventory/add_supplier.html'
    title = 'Edit Supplier'

    supplier = get_object_or_404(Supplier, id=supplier_id)
    # this form adds a new customer
    if request.method == 'POST':
        supplier_form = AddSupplierForm(request.POST, instance=supplier)
        if supplier_form.is_valid():
            form = supplier_form.save(commit=False)
            form.save()
            messages.success(request, "Supplier updated successfully")
            return redirect('./supplier-details')
    else:
        supplier_form = AddSupplierForm(instance=supplier)
    context = {
        'title': title,
        'supplier': supplier,
        'supplier_form': supplier_form,
    }
    return render(request, template, context)


@login_required
def delete_supplier(request, supl_id):
    supplier = get_object_or_404(Supplier, id=supl_id)
    supplier.delete()
    messages.success(request, "Supplier deleted successfully")
    return redirect('/suppliers')


@login_required
def customers_view(request):
    template = 'inventory/customers.html'
    title = 'Customers'

    all_customers = Client.objects.all()
    # this form adds a new customer
    if request.method == 'POST':
        customer_form = AddCustomerForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            messages.success(request, "New customer added successfully")
    else:
        customer_form = AddCustomerForm()
    context = {
        'title': title,
        'all_customers': all_customers,
        'customer_form': customer_form,
    }
    return render(request, template, context)


@login_required
def customer_details_view(request, customer_id):
    template = 'inventory/customer_details.html'
    title = 'Customer Details'

    customer_details = Client.objects.get(id=customer_id)
    context = {
        'title': title,
        'customer': customer_details,
    }
    return render(request, template, context)


@login_required
def add_customer_view(request):
    template = 'inventory/add_customer.html'
    title = 'Add Customer'

    all_customers = Client.objects.all()
    # this form adds a new customer
    if request.method == 'POST':
        customer_form = AddCustomerForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()
            messages.success(request, "New customer added successfully")
            return redirect('/customers')
    else:
        customer_form = AddCustomerForm()
    context = {
        'title': title,
        'all_customers': all_customers,
        'customer_form': customer_form,
    }
    return render(request, template, context)


@login_required
def update_customer_view(request, customer_id):
    template = 'inventory/add_customer.html'
    title = 'Customer'

    customer = get_object_or_404(Client, id=customer_id)
    # this form adds a new customer
    if request.method == 'POST':
        customer_form = AddCustomerForm(request.POST, instance=customer)
        if customer_form.is_valid():
            form = customer_form.save(commit=False)
            form.save()
            messages.success(request, "Customer updated successfully")
            return redirect('./customer-details')
    else:
        customer_form = AddCustomerForm(instance=customer)
    context = {
        'title': title,
        'customer': customer,
        'customer_form': customer_form,
    }
    return render(request, template, context)


@login_required
def delete_customer(request, cust_id):
    customer = get_object_or_404(Client, id=cust_id)
    customer.delete()
    messages.success(request, "Customer deleted successfully")
    return redirect('/customers')


# this code is unused
def all_products_export_csv(request):
    # exporting a csv file of all products
    response = HttpResponse(content_type='text/csv')
    response['content-disposition'] = 'attachment; filename=All products' + str(datetime.datetime.now()) + '.csv'
    writer = csv.writer(response)
    writer.writerow(['Product name', 'Category', 'Volume', 'In stock', 'Price per crate', 'pre_order level'])
    # products = Product.objects.filter(added_by=request.user)
    products = Product.objects.all()

    for product in products:
        writer.writerow([product.product_name, product.category, product.bottle_capacity, product.quantity_in_stock,
                         product.price_per_crate, product.reorder_level])

    return response


# end of unused code


# purchased products report
@login_required
def purchased_products(request):
    title = "Purchased products"
    template = "inventory/purchased_products_report.html"
    received_products = ReceiveProduct.objects.order_by('-published')
    context = {
        'title': title,
        'received_products': received_products,
    }
    return render(request, template, context)


# sold products report
@login_required
def sold_products(request):
    title = "Sold products"
    template = "inventory/sold_products_report.html"
    all_sold_products = SaleProduct.objects.all().order_by('-published')
    context = {
        'title': title,
        'all_sold_products': all_sold_products,
    }
    return render(request, template, context)


# update sold products
@login_required
def update_sold_product_view(request, product_id):
    template = 'inventory/issue_product.html'
    title = 'Update sold product'

    all_products = Product.objects.filter(active=True)
    product = get_object_or_404(SaleProduct, id=product_id)
    if request.method == 'POST':
        product_form = SellProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Sale updated successfully")
            return redirect('./')
    else:
        product_form = SellProductForm(instance=product)

    context = {
        'title': title,
        'all_products': all_products,
        'form': product_form,
    }
    return render(request, template, context)


# update received products
@login_required
def update_received_product_view(request, product_id):
    template = 'inventory/receive_product.html'
    title = 'Update received product'

    all_products = Product.objects.filter(active=True)
    product = get_object_or_404(ReceiveProduct, id=product_id)
    if request.method == 'POST':
        product_form = ReceiveProductForm(request.POST, instance=product)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, "Received product updated successfully")
            return redirect('../')
    else:
        product_form = ReceiveProductForm(instance=product)

    context = {
        'title': title,
        'all_products': all_products,
        'form': product_form,
    }
    return render(request, template, context)
