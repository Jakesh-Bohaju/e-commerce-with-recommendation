from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, ListView, DeleteView

from ecomadmin.forms import CategoryForm
from store.models import Category


# Create your views here.
class AdminView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            pass
        except Exception as e:
            print(e)
        return context


class CategoryFormView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "forms/category_form.html"
    form_class = CategoryForm
    model = Category
    success_url = reverse_lazy('dashboard:category')

    def form_invalid(self, form):
        return render(self.request, 'forms/category_form.html', {
            'form': form,
        })


class CategoryView(LoginRequiredMixin, ListView):
    template_name = "category.html"
    model = Category
    context_object_name = "categories"


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('dashboard:category')
