from django.urls import path
from . import views

urlpatterns = [
    #product
    path('', views.products, name='product-index'),
    path('add', views.product_add, name='product-add'),
    #path('<int:id>/edit', views.product_update, name='product-edit'),
    path('<int:id>/delete', views.product_delete, name='product-delete'),
    path('<int:id>/add-cart', views.product_add_cart, name='product-add-cart'),
]