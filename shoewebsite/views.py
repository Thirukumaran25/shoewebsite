from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.urls import reverse
from .forms import EnquiryForm,LoginForm,RegistrationForm
from django.contrib.auth import authenticate, login as auth_login
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CheckoutForm



# Create your views here.


def base(request):
    images=Logo.objects.all()
    return render(request,'base.html',
                  {'images':images,
                   })

def home(request):
    images=Logo.objects.all()
    images1=Banner.objects.all()
    images2=Homecategory.objects.all()
    images3=Homeproduct.objects.all()
    return render(request,'home.html',
                  {'images':images,
                   'images1':images1,
                   'images2':images2,
                   'images3':images3,
                   })

def about(request):
    images=Logo.objects.all()
    return render(request,'about.html',
                  {'images':images,
                   }
                )


def contact(request):
    images=Logo.objects.all()
    images1=Contact.objects.all()
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            request.session["enquiry_submitted"] = True
            return redirect("enquiry_thanks")
    else:
        form = EnquiryForm()

    return render(request,'contact.html',
                  {'images':images,
                   'images1':images1,
                   "form": form,
                   }
                )

def thanks_view(request):
    submitted = request.session.pop("enquiry_submitted", False)
    return render(request, "thanks.html", {"submitted":submitted})



def user_login(request):
    images = Logo.objects.all()
    form = LoginForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            auth_login(request, user)  
            return redirect(request.GET.get('next', 'home'))
        else:
            form.add_error(None, "Invalid credentials")

    return render(request, 'login.html', {
        'images': images,
        'form': form
    })


def register_view(request):
    images = Logo.objects.all()
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = user.username
        user.save()
        return redirect("login")
    return render(request, "register.html", {
        'images': images,
        "form": form,
        })


@login_required
def cart(request):
    images = Logo.objects.all()

    if request.method == 'POST':
        pid = request.POST.get('product_id')
        qty = request.POST.get('quantity')
        size = request.POST.get('size')
        color = request.POST.get('color')

        # Basic validation
        if not pid:
            messages.error(request, "Product ID is missing.")
            return redirect('women')

        product = Product.objects.filter(id=pid).first()
        if not product:
            messages.error(request, "Product not found.")
            return redirect('women')

        # Save to CartItem
        CartItem.objects.create(
            product=product,
            quantity=qty,
            size=size,
            color=color,
            user=request.user if request.user.is_authenticated else None
        )

        messages.success(request, f"{product.name} added to cart!")
        return redirect('cart')

    # Show cart page
    cart_items = CartItem.objects.filter(user=request.user) if request.user.is_authenticated else []
    total = sum([item.total_price for item in cart_items])

    return render(request, 'cart.html', {
        'images': images,
        'cart_items': cart_items,
        'total': total
    })



@login_required
def cart_view(request):
    images = Logo.objects.all()
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in cart_items)

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total,
        'images': images,
    })


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        size = request.POST.get('size', '41')
        color = request.POST.get('color', '')

        product = get_object_or_404(Product, id=product_id)

        CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            size=size,
            color=color,
        )
        messages.success(request, "Product added to cart.")
        return redirect('cart')

    return redirect('women')


def update_cart_quantity(request, item_id):
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

        if qty == 0:
            cart_item.delete()
            messages.info(request, 'Item removed from cart.')
        else:
            cart_item.quantity = qty
            cart_item.save()
            messages.success(request, 'Cart updated.')

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')




def mens(request):
    images = Logo.objects.all()
    qs = MenProduct.objects.all()
    q = request.GET.get("q")
    sort = request.GET.get("sort")

    for product in qs:
        product.color_list = product.colors.split(",") if product.colors else []

    if q:
        qs = qs.filter(Q(name__icontains=q)) 
    if sort == "price_asc":
        qs = qs.order_by("price_mrp")
    elif sort == "price_desc":
        qs = qs.order_by("-price_mrp")
    elif sort == "rating":
        qs = qs.order_by("-rating")
    return render(request, 'mens.html', {
                'images': images,
                "products": qs, 
                "sort": sort,
                "q": q,
            })


def kids(request):
    images = Logo.objects.all()
    qs = KidProduct.objects.all()
    q = request.GET.get("q")
    sort = request.GET.get("sort")

    for product in qs:
        product.color_list = product.colors.split(",") if product.colors else []

    if q:
        qs = qs.filter(Q(name__icontains=q)) 
    if sort == "price_asc":
        qs = qs.order_by("price_mrp")
    elif sort == "price_desc":
        qs = qs.order_by("-price_mrp")
    elif sort == "rating":
        qs = qs.order_by("-rating")
    return render(request, 'kids.html', {
                'images': images,
                "products": qs, 
                "sort": sort,
                "q": q,
            })


def womens(request): 
    images = Logo.objects.all()
    qs = Product.objects.all()
    q = request.GET.get("q")
    sort = request.GET.get("sort")

    for product in qs:
        product.color_list = product.colors.split(",") if product.colors else []

    if q:
        qs = qs.filter(Q(name__icontains=q)) 
    if sort == "price_asc":
        qs = qs.order_by("price_mrp")
    elif sort == "price_desc":
        qs = qs.order_by("-price_mrp")
    elif sort == "rating":
        qs = qs.order_by("-rating")
    return render(request, 'women.html', {
                'images': images,
                "products": qs, 
                "sort": sort,
                "q": q,
            })



def productdetail(request, pk: int): 
    images = Logo.objects.all()
    product = get_object_or_404(Product, pk=pk)
    thumbs = [product.image_url] * 4 
    colors = product.colors.split(",") if product.colors else []
    sizes = ['6', '7', '8', '9', '10']

    return render(request, "productdetail.html", {
                        'images': images,
                        "p": product,
                        "thumbs": thumbs,
                        "color_list": colors,
                        "sizes": sizes,
                    })

def menproductdetail(request, pk: int): 
    images = Logo.objects.all()
    product = get_object_or_404(MenProduct, pk=pk)
    thumbs = [product.image_url] * 4 
    colors = product.colors.split(",") if product.colors else []
    sizes = ['6', '7', '8', '9', '10']

    return render(request, "productdetail2.html", {
                        'images': images,
                        "p": product,
                        "thumbs": thumbs,
                        "color_list": colors,
                        "sizes": sizes,
                    })


def kidproductdetail(request, pk: int): 
    images = Logo.objects.all()
    product = get_object_or_404(KidProduct, pk=pk)
    thumbs = [product.image_url] * 4 
    colors = product.colors.split(",") if product.colors else []
    sizes = ['6', '7', '8', '9', '10']

    return render(request, "productdetail3.html", {
                        'images': images,
                        "p": product,
                        "thumbs": thumbs,
                        "color_list": colors,
                        "sizes": sizes,
                    })



@login_required
def checkout_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_items = CartItem.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            for item in cart_items:
                order = Order(
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    card_holder_name=form.cleaned_data.get('card_holder_name', ''),
                    card_number=form.cleaned_data.get('card_number', ''),
                    cvv=form.cleaned_data.get('cvv', ''),
                    expiry_date=form.cleaned_data.get('expiry_date', ''),
                    cash_on_delivery=form.cleaned_data.get('cash_on_delivery', False),
                    address_line_1=form.cleaned_data['address_line_1'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    landmark=form.cleaned_data.get('landmark', ''),
                    pincode=form.cleaned_data['pincode'],
                )
            order.save()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_success', order_id=order.id)
        else:
            print("Form errors:", form.errors)
    else:
        form = CheckoutForm(initial={'quantity': 1}) 
    
    return render(request, 'checkout.html', {
        'form': form,
        'product': product,
        'total_amount': product.price_mrp * form.initial.get('quantity', 1),
    })



@login_required
def checkout_from_cart(request):
    images = Logo.objects.all()
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.info(request, "Your cart is empty.")
        return redirect('cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = sum(item.total_price for item in cart_items)
            for item in cart_items:
                order = Order(
                    product=item.product,
                    quantity=item.quantity,
                    size=item.size,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    card_holder_name=form.cleaned_data.get('card_holder_name', ''),
                    card_number=form.cleaned_data.get('card_number', ''),
                    cvv=form.cleaned_data.get('cvv', ''),
                    expiry_date=form.cleaned_data.get('expiry_date', ''),
                    cash_on_delivery=form.cleaned_data.get('cash_on_delivery', False),
                    address_line_1=form.cleaned_data['address_line_1'],
                    city=form.cleaned_data['city'],
                    state=form.cleaned_data['state'],
                    landmark=form.cleaned_data.get('landmark', ''),
                    pincode=form.cleaned_data['pincode'],
                )
                order.save()

            cart_items.delete()
            messages.success(request, "Order placed successfully!")
            return redirect('order_success', order_id=order.id)
        else:
            print("Form errors:", form.errors)
    else:
        form = CheckoutForm()

    total_amount = sum(item.total_price for item in cart_items)

    return render(request, 'checkout1.html', {
        'images':images,
        'form': form,
        'cart_items': cart_items,
        'total_amount': total_amount,
    })


def order_success_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})

def order_track_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    events = [
        {"title": "Order Placed", "time": "May 21, 2025 | 03:45 pm", "icon": "cart", "complete": True},
        {"title": "Order Dispatched", "time": "May 22, 2025 | 11:45 am", "icon": "home", "complete": True},
        {"title": "Order in transit", "time": "Reached at Tenkasi, Post office", "icon": "truck", "complete": True},
        {"title": "Delivered successfully", "time": "Not delivered yet", "icon": "thumb", "complete": False},
    ]
    return render(request, 'track.html', {"order": order, "events": events})
