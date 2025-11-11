from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='pages_newarrivals'),
    path('products/', views.product_list_cate, name='product_Cate'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
]