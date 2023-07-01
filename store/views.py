from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login

from recommendation.data_collection import hybrid_recommendation
from vendor.models import EcommerceUser
from .cart import Cart
from .forms import OrderForm
from .models import Category, Product, Order, OrderItem, Review


def handlelogin(request):
    if request.method == "GET":
        return render(request, 'registration/login.html')

    elif request.method == "POST":
        uname = request.POST.get("username")
        pass1 = request.POST.get("pass1")
        myuser = authenticate(username=uname, password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, "Login Success")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/login')
    return render(request, 'registration/login.html')


def handlesignup(request):
    if request.method == "GET":
        return render(request, 'registration/signup.html')

    elif request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        confirmpassword = request.POST.get('pass2')
        # print(uname,email,password,confirmpassword)
        if password != confirmpassword:
            messages.warning(request, "Password is Incorrect")
            return redirect('/signup')
        try:
            if EcommerceUser.objects.get(username=uname):
                messages.info(request, 'UserName is Taken')
                return redirect('/signup')
        except:
            pass
        try:
            if EcommerceUser.objects.get(email=email):
                messages.info(request, 'Email is Taken')
                return redirect('/signup')
        except:
            pass
        myuser = EcommerceUser.objects.create_user(uname, email, password)
        myuser.save()
        messages.success(request, 'Signup Successful.Please Log In')
        return redirect('/login')
    return render(request, 'registration/signup.html')


@login_required
def add_to_cart(request, product_id):
    cart = Cart(request)
    cart.add(product_id)

    return redirect('frontpage')


@login_required
def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action:
        quantity = 1

        if action == 'decrease':
            quantity = -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)

    return redirect('cart_view')


@login_required
def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')


@login_required
def cart_view(request):
    cart = Cart(request)

    return render(request, 'store/cart_view.html', {
        'cart': cart
    })


@login_required
def checkout(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            total_price = 0

            for item in cart:
                product = item['product']
                print(product.price)
                print(int(item['quantity']))
                total_price += product.price * int(item['quantity'])

            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.save()

            for item in cart:
                product = item['product']
                quantity = int(item['quantity'])
                price = product.price * quantity

                item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity,
                                                created_by_id=request.user.id)
            cart.clear()

        return redirect('frontpage')
    else:
        form = OrderForm()

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
    })


def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(status=Product.ACTIVE).filter(
        Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'store/search.html', {
        'query': query,
        'products': products,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.filter(status=Product.ACTIVE)
    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
    review = Review.objects.filter(product_id=product.id)
    con_pid, coll_pid, hyb_pid = hybrid_recommendation(request, product.id)
    if not hyb_pid == None:
        recommended_products = Product.objects.filter(id__in=hyb_pid[:6])[1:]
    elif not coll_pid == None:
        recommended_products = Product.objects.filter(id__in=coll_pid[:6])[1:]
    else:
        recommended_products = Product.objects.filter(id__in=con_pid[:6])[1:]
    # return render(request, 'store/product_detail.html', {
    #     'product': product,
    #     'recommended_products': recommended_products
    # })

    if request.method == 'POST':
        rating = request.POST.get('rating', 3)
        content = request.POST.get('content', '')
        if content:
            reviews = Review.objects.filter(created_by=request.user, product=product)
            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            else:
                review = Review.objects.create(
                    product=product,
                    rating=rating,
                    content=content,
                    created_by=request.user
                )

    return render(request, 'store/product_detail.html', {
        'product': product,
        'reviews': review,
        'recommended_products': recommended_products
    })
