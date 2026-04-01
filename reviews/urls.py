from django.urls import path
from .views import (
    add_review,
    admin_reviews_preview,
    admin_reviews_all, admin_reviews_page
)

app_name = 'reviews'

urlpatterns = [
    path('add/<str:ma_san_pham>/', add_review, name='add_review'),

    path('api/admin/preview/', admin_reviews_preview, name='admin_reviews_preview'),
    path('api/admin/all/', admin_reviews_all, name='admin_reviews_all'),
    
    path('admin/', admin_reviews_page, name='admin_reviews_page'),
]