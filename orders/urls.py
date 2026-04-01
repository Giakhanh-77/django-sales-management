from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DonHangViewSet, LichSuGiaoDichViewSet, order_list

router = DefaultRouter()
router.register(r'donhang', DonHangViewSet, basename='donhang')
router.register(r'lichsugiaodich', LichSuGiaoDichViewSet, basename='lichsugiaodich')

urlpatterns = [
    path('', include(router.urls)),
    path('order_list/', order_list, name='order_list'),
]
