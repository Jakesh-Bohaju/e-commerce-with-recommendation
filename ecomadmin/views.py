from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DeleteView, UpdateView

from ecomadmin.forms import CategoryForm
from store.models import Category, Product, Order, OrderItem
from vendor.models import VendorDetail


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


# Create your views here.
# @staff_member_required
class AdminView(LoginRequiredMixin, AdminRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            pass
        except Exception as e:
            print(e)
        return context


class CategoryFormView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    template_name = "forms/category_form.html"
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('dashboard:category')

    def form_invalid(self, form):
        return render(self.request, 'forms/category_form.html', {
            'form': form,
        })


class CategoryView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "category.html"
    model = Category
    context_object_name = "categories"


class CategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('dashboard:category')


class ProductView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "product.html"
    model = Product
    context_object_name = "products"


class ProductDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('dashboard:product')


# class VendorView(LoginRequiredMixin, AdminRequiredMixin, ListView):
#     template_name = "vendor.html"
#     model = VendorDetail
#     context_object_name = "vendors"
#
#
# class VendorUpdateFormView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
#     template_name = "forms/category_form.html"
#     model = VendorDetail
#     fields = ["category_title"]
#     success_url = reverse_lazy('dashboard:vendor_update_form')
#
#     def form_invalid(self, form):
#         return self.render_to_response(self.get_context_data(form=form))
#
#
# class VendorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
#     model = VendorDetail
#     success_url = reverse_lazy('dashboard:vendor')


class OrderView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "order.html"
    model = Order
    context_object_name = "orders"


class OrderUpdateFormView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    # template_name = "forms/category_form.html"
    model = Order
    fields = ["is_paid"]
    success_url = reverse_lazy('dashboard:order')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# class OrderDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
#     model = Order
#     success_url = reverse_lazy('dashboard:order')


class TrackingView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "tracking.html"
    model = OrderItem
    context_object_name = "order_items"


class TrackingUpdateFormView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    template_name = "forms/category_form.html"
    model = OrderItem
    fields = ["category_title"]
    success_url = reverse_lazy('dashboard:tracking')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

# class TrackingDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
#     model = OrderItem
#     success_url = reverse_lazy('dashboard:tracking')


# class TransactionView(LoginRequiredMixin, AdminRequiredMixin, ListView):
#     template_name = "tracking.html"
#     model = OrderItem
#     context_object_name = "transactions"
