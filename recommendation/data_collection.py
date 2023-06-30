import os

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import pandas as pd
import json

from store.models import Product, Review
from vendor.models import EcommerceUser


def data_collection(request):
    try:
        product = Product.objects.filter(status='Active')
        # ecommerce_user = EcommerceUser.objects.filter(is_vendor=False, is_superuser=False)
        review = Review.objects.all()
        product_json = json.dumps(list(product.values()))
        # ecommerce_user_json = json.dumps(list(ecommerce_user.values()), cls=DjangoJSONEncoder)
        review_json = json.dumps(list(review.values()), cls=DjangoJSONEncoder)
        with open(os.path.abspath("recommendation/dataset/product.json"), "w") as file:
            file.write(product_json[1:-1])
        # with open(os.path.abspath("recommendation/dataset/user.json"), "w") as file:
        #     file.write(ecommerce_user_json[1:-1])
        with open(os.path.abspath("recommendation/dataset/review.json"), "w") as file:
            file.write(review_json[1:-1])
        return product, review

    except:
        pass

    return None

# def data_cleaning(request):
#     product, user, review = data_collection(request)
#     product_json = serializers.serialize('json', product)
#     ecommerce_user_json = serializers.serialize('json', user)
#     review_json = serializers.serialize('json', review)
#
#     print("product ", product_json)
#     print("user ", ecommerce_user_json)
#     print("review ", review_json)
