from django.urls import path
from .views import (
    dashboard_view,
    landing_view,
    
    register_view,
    login_view,
    logout_view,
    
)
urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', landing_view, name='landing'),
]
