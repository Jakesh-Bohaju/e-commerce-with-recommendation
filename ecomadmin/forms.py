from django import forms

from store.models import Category, OrderItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'title'
        ]
