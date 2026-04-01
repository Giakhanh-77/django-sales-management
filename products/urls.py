from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SanPhamViewSet, DanhMucViewSet,
    product_list, product_add, product_edit, product_delete, top_products
)
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'sanpham', SanPhamViewSet, basename='sanpham')
router.register(r'danhmuc', DanhMucViewSet, basename='danhmuc')

urlpatterns = [
    path('', include(router.urls)),

    path('product_list/', product_list, name='product_list'),
    path('product_add/', product_add, name='product_add'),
    path('product_edit/<int:id>/', product_edit, name='product_edit'),  
    path('product_delete/<int:id>/', product_delete, name='product_delete'),
    path('top-products/', top_products, name='top-products'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
