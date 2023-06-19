from django.urls import path

from ecomadmin.views import AdminView

app_name = 'dashboard'
urlpatterns = [
    path('', AdminView.as_view(), name="admin_index"),
]
