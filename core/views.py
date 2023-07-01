from django.shortcuts import render

from recommendation.data_collection import recommend_popularity_based
from store.models import Product


def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE).order_by('?')[:16]
    popular_products = recommend_popularity_based(request)
    return render(request, 'core/index.html', {
        'products': products,
        'popular_products': popular_products
    })
