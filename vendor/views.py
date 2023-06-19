from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import EcommerceUser

from store.forms import ProductForm
from store.models import Product, Order, OrderItem


def handlesellersignup(request):
    if request.method == "GET":
        return render(request, 'registration/sellersignup.html')

    if request.method == 'POST':
        print(request.get_full_path())
        uname = request.POST.get('username')
        email = request.POST.get('email')
        # brand = request.POST.get('BrandName')
        # pan = request.POST.get('PAN')
        password = request.POST.get('pass1')
        confirmpassword = request.POST.get('pass2')
        if password != confirmpassword:
            messages.warning(request, "Password is Incorrect")
            return redirect('/vendor/seller-signup')
        try:
            if EcommerceUser.objects.get(username=uname):
                messages.info(request, 'UserName is Taken')
                return redirect('/vendor/seller')
        except:
            pass
        try:
            if EcommerceUser.objects.get(email=email):
                messages.info(request, 'Email is Taken')
                return redirect('/vendor/seller')
        except:
            pass
        # try:
        #     if EcommerceUser.objects.get(BrandName=brand):
        #         messages.info(request, 'BrandName is Taken')
        #         return redirect('/ecomadmin/seller')
        # except:
        #     pass
        # try:
        #     if EcommerceUser.objects.get(PAN=pan):
        #         messages.info(request, 'Pan is Taken')
        #         return redirect('/ecomadmin/seller')
        # except:
        #     pass

        is_vendor = False
        if request.get_full_path() == '/vendor/seller-signup':
            is_vendor = True
        myuser = EcommerceUser.objects.create_user(uname, email, password, is_vendor=is_vendor)
        myuser.save()
        return render(request, 'userprofile/seller.html')
    return render(request, 'registration/sellersignup.html')


def handlesellerlogin(request):
    if request.method == "GET":
        return render(request, 'registration/sellerlogin.html')

    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        myuser = authenticate(username=uname, password=pass1)
        if myuser is not None and myuser.is_vendor:
            login(request, myuser)
            messages.success(request, 'login success')
            return redirect('/vendor/seller')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('/vendor/seller-login')
    return render(request, 'registration/sellerlogin.html')


@login_required
def vendor_detail(request, pk):
    if request.user.is_authenticated and request.user.is_vendor:

        user = EcommerceUser.objects.get(pk=pk)
        products = user.products.filter(status=Product.ACTIVE)

        return render(request, 'userprofile/vendor_detail.html', {
            'user': user,
            'products': products,

        })
    else:
        return render(request, 'registration/sellerlogin.html')


@login_required
def seller(request, *args, **kwargs):
    if request.user.is_authenticated and request.user.is_vendor:
        # products = request.user.products.exclude(status=Product.DELETED)
        try:
            products = request.user.products.exclude(status=Product.DELETED)
            order_items = OrderItem.objects.filter(product__user=request.user)
            for i in order_items:
                print(i)
            return render(request, 'userprofile/seller.html', {
                'products': products,
                'order_items': order_items,
            })
        except:
            pass
    else:
        return render(request, 'registration/sellerlogin.html')


@login_required
def seller_order_detail(request, pk, *args, **kwargs):
    if request.user.is_authenticated and request.user.is_vendor:

        order = get_object_or_404(Order, pk=pk)
        # orderitem = OrderItem.objects.get(order_id=order.id)

        return render(request, 'userprofile/seller_order_detail.html', {
            'orderitem': order,
        })
    else:
        return render(request, 'registration/sellerlogin.html')


@login_required
def add_product(request, *args, **kwargs):
    if request.user.is_authenticated and request.user.is_vendor:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)

            if form.is_valid():
                title = request.POST.get('title')
                product = form.save(commit=False)
                product.user = request.user
                product.slug = slugify(title)
                product.save()

                messages.success(request, 'The Product was added!')
                return redirect('/ecomadmin/seller')
            else:
                print(form.errors)

        else:
            form = ProductForm()

        return render(request, 'userprofile/add_product.html', {
            'title': 'Add Product',
            'form': form
        })
    else:
        return render(request, 'registration/sellerlogin.html')


@login_required
def edit_product(request, pk, *args, **kwargs):
    if request.user.is_authenticated and request.user.is_vendor:

        product = Product.objects.filter(user=request.user).get(pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)

            if form.is_valid():
                form.save()

                messages.success(request, 'The Changes was added!')
                return redirect('seller')

        else:
            form = ProductForm(instance=product)
            return render(request, 'userprofile/add_product.html', {
                'title': 'Edit Product',
                'product': product,
                'form': form
            })
    else:
        return render(request, 'registration/sellerlogin.html')


@login_required
def delete_product(request, pk, *args, **kwargs):
    if request.user.is_authenticated and request.user.is_vendor:

        product = Product.objects.filter(user=request.user).get(pk=pk)
        product.status = Product.DELETED
        product.save()

        messages.success(request, 'The Product was deleted!')
        return redirect('seller')
    else:
        return render(request, 'registration/sellerlogin.html')