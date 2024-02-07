from django.urls import path
from . import views

urlpatterns = [
    #product
    path('', views.sales, name='sale-index'),
    path('add', views.sale_add, name='sale-add'),
    #path('<int:id>/edit', views.sale_update, name='sale-edit'),
    #path('<int:id>/delete', views.sale_delete, name='sale-delete'),
]