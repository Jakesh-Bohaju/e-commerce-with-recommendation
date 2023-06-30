from django.shortcuts import render

from store.models import Product

def frontpage(request):
    products = Product.objects.filter(status=Product.ACTIVE).order_by('?')
    return render(request,'core/frontpage.html', {
        'products': products
    })