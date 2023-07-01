from django.shortcuts import render

from recommendation.data_collection import recommend_popularity_based
from store.models import Product, Category


def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE).order_by('?')[:16]
    categories = Category.objects.all()
    popular_products = recommend_popularity_based(request)
    return render(request, 'core/index.html', {
        'products': products,
        'popular_products': popular_products,
        'categories':categories,
    })
