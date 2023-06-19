from django.urls import path

from . import views

# app_name = 'vendor'

urlpatterns = [
    path('seller-login', views.handlesellerlogin, name='handlesellerlogin'),
    path('seller-signup', views.handlesellersignup, name='handlesellersignup'),
    path('<int:pk>/', views.seller, name='seller'),
    path('seller/order-detail/<int:pk>/', views.seller_order_detail, name='seller_order_detail'),
    path('<int:pk>/add-product/', views.add_product, name='add_product'),
    path('seller/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('seller/delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]
