from django.urls import path

from ecomadmin.views import *

app_name = 'dashboard'
urlpatterns = [
    path('', AdminView.as_view(), name="admin_index"),

    # category CRD (Create, Read, Delete)
    path('insert/category', CategoryFormView.as_view(), name="category_form"),
    path('category', CategoryView.as_view(), name="category"),
    path('delete/category/<slug:slug>/', CategoryDeleteView.as_view(), name='delete_category'),

]
