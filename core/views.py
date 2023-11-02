from core.forms import *
from django.contrib import messages
from django.shortcuts import *
from core.models import *
from django.contrib.auth import *
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def checkout_page(request):
    if CheckoutAddress.objects.filter(user=request.user).exists():
        return render(request, 'core/checkout.html', {'payment_allow':'allow'})
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        try:
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('Country')
                zip_code = form.cleaned_data.get('zip_code')

                checkout_address = CheckoutAddress(
                    user = request.user,
                    street_address = street_address,
                    apartment_address = apartment_address,
                    Country = country,
                    zip_code = zip_code,
                )
                checkout_address.save()
                print("It Shoult render the summary page")
                return render (request, 'core/checkout.html', {'payment_allow':'allow'})
        except ObjectDoesNotExist:
            messages.warning(request, "Failed Checkout")
            return redirect('checkout_page')

    else:
        form = CheckoutForm()
        return render(request, 'core/checkout.html', {'form':form})


def index (request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products':products})


@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            print("Saved Successfully")
            messages.success(request, "Product Added Successfully")
            return redirect ('/')
    else:
        print ("not working")
        form = ProductForm()
    return render (request,'core/add_product.html', {'form':form})


def product_desc(request, pk):
    product = Product.objects.get(pk=pk)
    return render (request, 'core/product_desc.html', {'product':product})


@login_required
def add_to_cart(request, pk):
    #get that particular product
    product = Product.objects.get(pk=pk)
    if product.product_available_count < 1:
        messages.info(request, "Sorry Product is out of stock")
        return redirect ("orderlist")
    else:
        #Create order item
        order_item , created = OrderItem.objects.get_or_create(
        product = product,
        user = request.user,
        ordered = False,
        sale_in = product.sale_in,
    )

    #Get query set of order object of particular user 
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            if product.product_available_count < 1:
                messages.info(request, "Sorry Product is out of stock")
            else:
                order_item.quantity += 1
                order_item.save()
                product.product_available_count -= 1
                product.save()
                messages.info(request, "Added quantity item")
        else:
            order.items.add(order_item)
            product.product_available_count -= 1
            product.save()
            messages.info(request, "Item added to cart")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to cart")

    return redirect ("product_desc", pk=pk)

@login_required
def orderlist (request):
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, 'core/orderlist.html', {'order':order})
    return render(request, 'core/orderlist.html', {'message':"Your cart is empty"})



@login_required
def add_item(request, pk):
    #get that particular product
    product = Product.objects.get(pk=pk)
    #Create order item
    order_item , created = OrderItem.objects.get_or_create(
    product = product,
    user = request.user,
    ordered = False,
    )

    #Get query set of order object of particular user 
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Added quantity item")
            else: 
                messages.info(request, "Sorry Product is out of stock")
            return redirect ("orderlist")

        else:
            order.items.add(order_item)
            messages.info(request, "Iem added to cart")
            return redirect ("orderlist", pk=pk)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item added to cart")
        return redirect ("orderlist", pk=pk)



@login_required
def remove_item (request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(
        user = request.user, 
        ordered = False, 
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item = OrderItem.objects.filter(
                product= item,
                user = request.user,
                ordered = False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                item.product_available_count +=1
                item.save()
                order_item.save()
            else:
                order_item.delete()
                item.product_available_count +=1
                item.save()
            messages.info(request, "Item quantity updated successfully")
            return redirect('orderlist')

        else:
            messages.info(request, "This item is not in your item list")
            return redirect("orderlist")
    else:
        messages.info(request, "You do not have any order")
        return redirect("orderlist")
