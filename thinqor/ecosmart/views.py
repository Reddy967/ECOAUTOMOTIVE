from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from .models import *
import razorpay
from django.conf import settings

# Create your views here.

def navbar(request):
    if request.session.get('user.id'):
        user_id = request.session.get('user.id')
        context = {
            'user_id': user_id
        }
    return render(request, 'navbar.html', context)


def products(request):
    user_id = request.session.get('user.id')
    products = Products.objects.all()
    context = {
        'user_id': user_id,
        'products': products
    }
    return render(request, 'products.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        password = request.POST.get('password')
        users = Register()
        users.username = username
        users.email = email
        users.phonenumber = phonenumber
        users.password = password
        users.save()
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(email=email, password=password)
            user_id = user.id
            request.session['user.id'] = user_id
            print(user_id)
            return redirect('contact')
        except Register.DoesNotExist:
            return HttpResponse('Invalid')
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def home(request):
    return render(request, 'home.html')


def product_cart(request, user_id):
    if request.method == 'POST':
        product_id = request.POST.get('product.id')
        product = Products.objects.get(id=product_id)

        cart_item = Product_Cart(user_id=user_id, product=product)
        cart_item.save()

        return redirect('navbar')

    return render(request, 'products.html')


def product_book(request, user_id):
    if request.method == 'POST':
        product_id = request.POST.get('product.id')
        product = Products.objects.get(id=product_id)

        book_item = Product_Book(user_id=user_id, product=product)
        book_item.save()

        return redirect('booked_products')

    return render(request, 'products.html')

def booked_products(request):
    user_id = request.session.get('user.id')
    booked_items = Product_Book.objects.filter(user_id=user_id)

    booked_products_info = []
    for item in booked_items:
        product = Products.objects.get(id=item.product_id)
        booked_products_info.append({
            'product': product,
            'user_id': item.user_id
        })

    context = {
        'booked_products_info': booked_products_info
    }
    return render(request, 'booked_products.html', context)

def cart_view(request, user_id):
    #user_id = request.session.get('user.id')
    cart_items = Product_Cart.objects.filter(user_id=user_id)

    cart_products_info = []
    for item in cart_items:
        product = Products.objects.get(id=item.product_id)
        cart_products_info.append({
            'product': product,
            'user_id': item.user_id
        })

    context = {
        'cart_products_info': cart_products_info
    }

    return render(request, 'cart_view.html', context)

from django.http import JsonResponse

def get_cart_item_count(request):
    user_id = request.session.get('user.id')
    cart_item_count = Product_Cart.objects.filter(user_id=user_id).count()

    data = {
        'cart_item_count': cart_item_count
    }

    return JsonResponse(data)




def shipping_address(request):
    user_id = request.session.get('user.id')
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')

        shipping_address = ShippingAddress(
            user_id=user_id,
            name=name,
            email=email,
            phonenumber=phonenumber,
            address=address,
            state=state,
            city=city,
            postal_code=postal_code
        )
        shipping_address.save()
        return redirect('contact')


    return render(request, 'shipping_address.html')


def checkout(request):
    user_id = request.session.get('user.id')
    user_shipping_addresses = ShippingAddress.objects.filter(user_id=user_id)
    booked_products = Product_Book.objects.filter(user_id=user_id)

    total_amount = 0
    discount_amount = 0
    discount_coupon = None

    if 'coupon_code' in request.POST:
        coupon_code = request.POST.get('coupon_code')
        try:
            discount_coupon = DiscountCoupon.objects.get(code=coupon_code)
            discount_amount = discount_coupon.amount
        except DiscountCoupon.DoesNotExist:
            messages.error(request, 'Invalid coupon code.')

    if request.method == 'POST':
        for booked_product in booked_products:
            quantity_booked = int(request.POST.get(f'quantity_{booked_product.product.id}', 0))
            if quantity_booked > 0:
                product_total_amount = booked_product.product.amount * quantity_booked
                discounted_total_amount = product_total_amount - (discount_amount * quantity_booked)

                selected_shipping_address_id = request.POST.get('shippingAddress')
                selected_shipping_address = ShippingAddress.objects.get(id=selected_shipping_address_id)

                checkout = Checkout.objects.create(
                    user_id=user_id,
                    product_id=booked_product.product.id,
                    user_shipping_address=selected_shipping_address,
                    quantity=quantity_booked,
                    total_amount=discounted_total_amount
                )
                checkout.save()
        return redirect('payment')

    context = {
        'user_shipping_addresses': user_shipping_addresses,
        'booked_products': booked_products,
        'total_amount': total_amount,
        'discount_coupon': discount_coupon
    }
    return render(request, 'checkout.html', context)



def edit_shipping_address(request, address_id):
    if request.method == "POST":
        new_name = request.POST.get("new_name")
        new_email = request.POST.get("new_email")
        new_phonenumber = request.POST.get("new_phonenumber")
        new_address = request.POST.get("new_address")
        new_state = request.POST.get("new_state")
        new_city = request.POST.get("new_city")
        new_postal_code = request.POSt.get("new_postal_code")

        address = ShippingAddress.objects.get(id=address_id)
        address.name = new_name
        address.email = new_email
        address.phonenumber = new_phonenumber
        address.address = new_address
        address.state = new_state
        address.city = new_city
        address.postal_code = new_postal_code
        address.save()


        return JsonResponse({"message": "Address updated successfully"})
    else:
        return JsonResponse({"error": "Invalid request method"})

def remove_item(request,id):
    data = Product_Book.objects.filter(id=id).delete()
    return redirect('products')

def checkout_cart(request):
    user_id = request.session.get('user.id')
    user_shipping_addresses = ShippingAddress.objects.filter(user_id=user_id)
    cart_items = Product_Cart.objects.filter(user_id=user_id)
    total_amount = 0
    discount_amount = 0
    discount_coupon = None

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')

        # Check if a coupon code is provided
        if coupon_code:
            try:
                discount_coupon = DiscountCoupon.objects.get(code=coupon_code)
                discount_amount = discount_coupon.amount
            except DiscountCoupon.DoesNotExist:
                messages.error(request, 'Invalid coupon code.')

        # Iterate through cart items
        for cart_item in cart_items:
            quantity_booked = int(request.POST.get(f'quantity_{cart_item.product.id}', 0))
            if quantity_booked > 0:
                product_total_amount = cart_item.product.amount * quantity_booked
                discounted_total_amount = product_total_amount - (discount_amount * quantity_booked)

                selected_shipping_address_id = request.POST.get('shippingAddress')
                selected_shipping_address = ShippingAddress.objects.get(id=selected_shipping_address_id)

                checkout = Checkout_Cart.objects.create(
                    user_id=user_id,
                    product_id=cart_item.product.id,
                    user_shipping_address=selected_shipping_address,
                    quantity=quantity_booked,
                    total_amount=discounted_total_amount
                )
                checkout.save()


        return redirect('payment')

    context = {
        'user_shipping_addresses': user_shipping_addresses,
        'cart_items': cart_items,
        'total_amount': total_amount,
        'discount_coupon': discount_coupon
    }
    return render(request, 'checkout_cart.html', context)


def payment(request):
    user_id = request.session.get('user.id')
    total_amount = Checkout.objects.filter(user_id=user_id).aggregate(total_amount=models.Sum('total_amount'))['total_amount']

    if total_amount is None:
        total_amount = 0

    razoramount = int(total_amount * 100)

    try:
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        data = {
            "amount": razoramount,
            "currency": "INR",
            "receipt": "order_rcptid_12"
        }
        payment_response = client.order.create(data=data)
        print(payment_response)
        order_id = payment_response['id']
        order_status = payment_response['status']

        if order_status == 'created':
            payment = Payment(
                user_id=user_id,
                total_amount=total_amount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()

        return render(request, 'payment.html', {'razoramount': razoramount, 'order_id': order_id})

    except Exception as e:
        # Handle exceptions here, e.g., log the error and provide an error message to the user
        return render(request, 'error.html', {'error_message': str(e)})




def paymentdone(request):
    user_id = request.session.get('user.id')
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')

    # Use filter instead of get
    payments = Payment.objects.filter(razorpay_order_id=order_id)

    # Check if any payments match the order_id
    if payments.exists():
        # Take the first payment that matches (you can adjust this logic if needed)
        payment = payments.first()

        # Rest of your code remains unchanged
        payment.paid = True
        payment.razorpay_payment_id = payment_id
        payment.save()

        checkout_items = Checkout.objects.filter(user_id=user_id)

        for item in checkout_items:
            OrderPlaced(user_id=user_id, product=item.product, quantity=item.quantity, payment=payment).save()
            item.delete()

        return redirect('products')
    else:
        # Handle the case where no payment matches the order_id
        return HttpResponse("Payment not found")
