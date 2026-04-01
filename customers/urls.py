from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import KhachHangViewSet, customer_list, login_customer,register_customer, logout_customer

router = DefaultRouter()
router.register(r'khachhang', KhachHangViewSet)

urlpatterns = [
    path('customer_list/', customer_list, name='customer_list'),
    path('', include(router.urls)),
     path('register/', register_customer, name='register_cus'),
    path('login/', login_customer, name='login_cus'),
    path('logout/', logout_customer, name='logout_cus'),
]