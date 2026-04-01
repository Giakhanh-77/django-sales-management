from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import KhoHangViewSet, inventory_list

router = DefaultRouter()
router.register(r'khohang', KhoHangViewSet, basename='khohang')

urlpatterns = [
    path('inventory_list/', inventory_list, name='inventory_list'),
    path('', include(router.urls)),   
]
