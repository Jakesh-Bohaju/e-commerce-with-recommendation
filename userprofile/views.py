from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Userprofile

from store.forms import ProductForm
from store.models import Product, Order, OrderItem

def handlesellersignup(request):
    if request.method == "GET":
        return render(request,'registration/sellersignup.html')
    
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        brand=request.POST.get('BrandName')
        pan=request.POST.get('PAN')
        password=request.POST.get('pass1')
        confirmpassword=request.POST.get('pass2')
        if password!=confirmpassword:
           messages.warning(request,"Password is Incorrect")
           return redirect('/admin/seller-signup')
        try:
           if User.objects.get(username=uname):
                messages.info(request,'UserName is Taken')
                return redirect('/admin/seller')
        except:
           pass
        try:
           if User.objects.get(email=email):
                messages.info(request,'Email is Taken')
                return redirect('/admin/seller')
        except:
           pass
        try:
           if User.objects.get(BrandName=brand):
                messages.info(request,'BrandName is Taken')
                return redirect('/admin/seller')
        except:
           pass
        try:
           if User.objects.get(PAN=pan):
                messages.info(request,'Pan is Taken')
                return redirect('/admin/seller')
        except:
           pass
        myuser= User.objects.create_user(uname, email, password)
        myuser.save()
        return HttpResponse('Seller Signup Success')
    return render(request,'registration/sellersignup.html')

def handlesellerlogin(request):
    if request.method == "GET":
        return render(request,'registration/sellerlogin.html')
    
    if request.method=='POST':
       uname=request.POST.get('username')
       pass1=request.POST.get('pass1')
       myuser=authenticate(username=uname,password=pass1)
       if myuser is not None:
           login(request,myuser)
           messages.success(request,'login success')
           return redirect('/admin/seller')
       else:
           messages.error(request,'Invalid Credentials')
           return redirect('/admin/seller-login')
    return render(request,'registration/sellerlogin.html')


def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)
    products = user.products.filter(status=Product.ACTIVE)

    return render(request, 'userprofile/vendor_detail.html',{
        'user': user,
        'products' : products,

    })
    
def seller(request):
    products = request.user.products.exclude(status=Product.DELETED)
    print("product user " , products)
    print(request.user)
    order_items = OrderItem.objects.all()
    for i in order_items:
        print(i)
    return render(request, 'userprofile/seller.html',{
        'products': products,
        'order_items': order_items,
    })

def seller_order_detail(request,pk):
    order = get_object_or_404(Order, pk=pk)
    orderitem = OrderItem.objects.get(order_id=order.id)
    print(orderitem.quantity)
    print(orderitem.product.title)
    print(orderitem.price)

    return render(request, 'userprofile/seller_order_detail.html',{
        'orderitem': orderitem,
    })


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()

            messages.success(request, 'The Product was added!')
            return redirect('/admin/seller')
        else:
            print(form.errors)

    else:
        form = ProductForm()

    return render(request, 'userprofile/add_product.html',{
        'title' : 'Add Product',
        'form' : form
    })
    
def edit_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()

            messages.success(request, 'The Changes was added!')
            return redirect('seller')

    else:
       form = ProductForm(instance=product)
    return render(request, 'userprofile/add_product.html',{
        'title' : 'Edit Product',
        'product' : product,
        'form' : form
    })

def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.status = Product.DELETED
    product.save()

    messages.success(request, 'The Product was deleted!')
    return redirect('seller')
