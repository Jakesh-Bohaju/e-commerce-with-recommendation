from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, TemplateView, CreateView, DetailView

from ecomadmin.models import About
from recommendation.data_collection import hybrid_recommendation
from vendor.models import EcommerceUser
from .cart import Cart
from .forms import OrderForm, ProfileForm
from .models import Category, Product, Order, OrderItem, Review, CustomerProfile


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
    try:
        cart = Cart(request)
        about = About.objects.all().first()
        categories = Category.objects.all()

        return render(request, 'store/cart_view.html', {
            'cart': cart,
            'about': about,
            'categories': categories,

        })
    except:
        pass


@login_required
def checkout(request, pk):
    try:
        cart = Cart(request)
        about = About.objects.all().first()
        categories = Category.objects.all()
        profile = CustomerProfile.objects.get(user_id=pk)

        if request.method == 'POST':
            form = OrderForm(request.POST)

            if form.is_valid():
                total_price = 0

                for item in cart:
                    product = item['product']
                    # print(product.price)
                    # print(int(item['quantity']))
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
            'about': about,
            'categories': categories,
            'profile': profile,

        })
    except:
        return render(request, 'store/profile_form.html', )


def search(request):
    try:
        query = request.GET.get('query', '')
        products = Product.objects.filter(status=Product.ACTIVE).filter(
            Q(title__icontains=query) | Q(description__icontains=query))
        about = About.objects.all().first()
        categories = Category.objects.all()

        return render(request, 'store/search.html', {
            'query': query,
            'products': products,
            'about': about,
            'categories': categories,

        })
    except:
        pass


def category_detail(request, slug):
    try:
        category = get_object_or_404(Category, slug=slug)
        products = category.products.filter(status=Product.ACTIVE)
        about = About.objects.all().first()
        categories = Category.objects.all()

        return render(request, 'store/category_detail.html', {
            'category': category,
            'products': products,
            'about': about,
            'categories': categories,
        })
    except:
        pass

def product_detail(request, category_slug, slug):
    try:
        product = get_object_or_404(Product, slug=slug, status=Product.ACTIVE)
        categories = Category.objects.all()

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

        review = Review.objects.filter(product_id=product.id)
        random_products = Product.objects.filter(category_id=product.category.id, status='Active').order_by('-id')
        about = About.objects.all().first()
        con_pid, coll_pid, hyb_pid = hybrid_recommendation(request, product.id)
        if not hyb_pid == None:
            hyb_pid = hyb_pid[1:6]
            recommended_products = Product.objects.filter(id__in=hyb_pid[1:6], status='Active')
        elif not coll_pid == None:
            recommended_products = Product.objects.filter(id__in=coll_pid[1:6], status='Active')
        else:
            recommended_products = Product.objects.filter(id__in=con_pid[1:6], status='Active')

        return render(request, 'store/product_detail.html', {
            'product': product,
            'random_products': random_products,
            'reviews': review,
            'recommended_products': recommended_products,
            'about': about,
            'categories': categories,

        })
    except:
        pass


class ProductListView(ListView):
    template_name = "store/product_list.html"
    model = Product
    queryset = Product.objects.filter(status='Active')
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['about'] = About.objects.all().first()
            context['categories'] = Category.objects.all()
        except:
            pass
        return context


class AddProfileView(LoginRequiredMixin, CreateView):
    template_name = "store/profile_form.html"
    form_class = ProfileForm
    model = CustomerProfile
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['about'] = About.objects.all().first()
            context['categories'] = Category.objects.all()
        except:
            pass
        return context

    def form_invalid(self, form):
        return render(self.request, 'store/profile_form.html', {
            'form': form,
        })

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})


class ProfileView(LoginRequiredMixin, DetailView):
    template_name = "store/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['about'] = About.objects.all().first()
            context['categories'] = Category.objects.all()
            context['profile'] = CustomerProfile.objects.get(user=self.request.user.id)
            context['order_items'] = OrderItem.objects.filter(created_by=self.request.user.id)
        except:
            pass
        return context

    def get_queryset(self):
        return EcommerceUser.objects.filter(id=self.kwargs.get('pk'))


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    template_name = "store/update_profile_form.html"
    fields = ['first_name', 'last_name', 'address', 'mobileNo', 'photo', 'user']
    model = CustomerProfile

    # context_object_name = 'con_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['about'] = About.objects.all().first()
            context['categories'] = Category.objects.all()
            context['profile'] = CustomerProfile.objects.get(user=self.request.user.id)
        except:
            pass
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_queryset(self):
        return CustomerProfile.objects.filter(id=self.kwargs.get('pk'))

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})
