from django.contrib import admin
from django.shortcuts import render
from django.urls import path,  include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

def home(request):
    return render(request, 'home.html')
urlpatterns = [
    path('dashboard/', include('users.urls'), name='dashboard'),   
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),        
    path('api/users/', include('users.urls')),
    path('api/products/', include('products.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/customers/', include('customers.urls')),
    path('api/inventory/', include('inventory.urls')),
    path('api/reports/', include('reports.urls')),
    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('store/', include('buystore.urls')),
    path('reviews/', include('reviews.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)