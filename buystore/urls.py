from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name='store_cart'),
    path('cart/update/', views.update_cart, name='store_update_cart'),

    path('checkout/', views.checkout, name='store_checkout'),
    path('order_history/', views.order_history, name='store_order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='store_order_detail'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='store_cancel_order'),

    path('', views.product_list, name='store_product_list'),
    path('product/<str:ma_san_pham>/', views.product_detail, name='store_product_detail'),
    path('product/buy/<str:ma_san_pham>/', views.buy_now, name='store_buy_now'),
    path('category/<int:category_id>/', views.product_by_category, name='store_category'),
]
