from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_home, name='report_home'),
    path('sales/', views.sales_report, name='sales_report'),
    path('top_products/', views.top_products_report, name='top_products_report'),
    path('doanh-thu-hom-nay/', views.doanh_thu_hom_nay, name='doanh_thu_hom_nay'),
    path('tong-hang-da-ban/', views.tong_hang_da_ban, name='tong_hang_da_ban'),
    path('stock-alerts/', views.stock_alerts, name='stock_alerts'),
    path('latest-customers/', views.latest_customers, name='latest_customers'),
    path('pending-orders/', views.pending_orders, name='pending-orders'),
    # path('monthly-revenue/', views.monthly_revenue, name='monthly_revenue'),
    path('daily-revenue/', views.daily_revenue, name='daily_revenue'),
]

