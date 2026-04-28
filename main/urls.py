from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.products_list, name='products_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('brands/', views.brands_list, name='brands_list'),
    path('about/', views.about, name='about'),
]
