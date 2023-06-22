import itertools

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DeleteView, UpdateView

from ecomadmin.forms import CategoryForm
from store.models import Category, Product, Order, OrderItem
from vendor.models import VendorDetail
import operator


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
            context['product_count'] = Product.objects.all().count()
            vendor_count = VendorDetail.objects.all().count()
            context['vendor_count'] = vendor_count
            un_verified_vendor_count = VendorDetail.objects.filter(verify_status=False).count()
            verified_vendor_count = VendorDetail.objects.filter(verify_status=True).count()
            context['un_verified_vendor_count'] = un_verified_vendor_count
            context['not_paid'] = Order.objects.filter(is_paid=False).count()
            context['new_order_count'] = OrderItem.objects.filter(tracking_status='Order Requested').count
            context['order_count'] = Order.objects.all().count()
            context['total_transaction'] = OrderItem.objects.all().aggregate(total=Sum('price'))
            un_verified_vendor_percent = un_verified_vendor_count / vendor_count * 100
            verified_vendor_percent = verified_vendor_count / vendor_count * 100

            # for Doughnut Charts
            vendor_data = [
                {"label": "Verified", "symbol": "O", "y": verified_vendor_percent},
                {"label": "Un-Verified", "symbol": "Si", "y": un_verified_vendor_percent},
            ]

            # For Bar Chart
            top_10_transaction_dict = {}
            vendors = VendorDetail.objects.all()
            for vendor in vendors:
                vendor_name = vendor.company_name
                total_amount = OrderItem.objects.filter(product__user__username=vendor.vendor.username).aggregate(
                    total=Sum('price'))
                for key, value in top_10_transaction_dict.copy().items():
                    if value is None:
                        top_10_transaction_dict[key] = 0
                top_10_transaction_dict[vendor_name] = total_amount[
                    'total']
            top_10_transaction_dict = dict(
                itertools.islice(
                    dict(sorted(top_10_transaction_dict.items(), key=operator.itemgetter(1), reverse=True)).items(),
                    10))
            print(top_10_transaction_dict)
            final_top_10_vendor_transaction_data = []
            for key, value in top_10_transaction_dict.items():
                final_top_10_vendor_transaction_data.append({"y": value, "label": key})

            context['vendor_data'] = vendor_data
            context['top_10_vendor_transaction_data'] = final_top_10_vendor_transaction_data
        except Exception as e:
            pass

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


class VendorView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "vendor.html"
    model = VendorDetail

    # context_object_name = "vendors"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verified_vendors'] = VendorDetail.objects.filter(verify_status=True)
        context['un_verified_vendors'] = VendorDetail.objects.filter(verify_status=False)
        return context


class VendorUpdateFormView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    # template_name = "forms/category_form.html"
    model = VendorDetail
    fields = ["verify_status"]
    success_url = reverse_lazy('dashboard:vendor')

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class VendorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = VendorDetail
    success_url = reverse_lazy('dashboard:vendor')


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
    template_name = "forms/tracking_update_form.html"
    model = OrderItem
    fields = ["tracking_status"]
    success_url = reverse_lazy('dashboard:tracking')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vendors'] = VendorDetail.objects.all()
        return context

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# class TrackingDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
#     model = OrderItem
#     success_url = reverse_lazy('dashboard:tracking')


class TransactionView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    template_name = "transaction.html"
    model = OrderItem
    context_object_name = "transactions"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_dict = {}
        vendors = VendorDetail.objects.all()
        order_items = OrderItem.objects.all()
        for vendor in vendors:
            vendor_name = vendor.company_name
            total_amount = OrderItem.objects.filter(product__user__username=vendor.vendor.username).aggregate(
                total=Sum('price'))
            transaction_dict[vendor_name] = total_amount[
                'total']
        context['transaction_list'] = transaction_dict

        return context
