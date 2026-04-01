from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets, filters, permissions
from .models import CustomUser
from .serializers import KhachHangSerializer
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


@staff_member_required(login_url='login')
def customer_list(request):
    return render(request, 'customers/khachhang.html')

class KhachHangViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-ngay_tao')
    serializer_class = KhachHangSerializer

    def perform_create(self, serializer):
        sdt = serializer.validated_data.get("sdt")

        serializer.save(
            username=sdt,  
            is_staff=False,
            is_superuser=False,
            is_active=True
        )
    

def register_customer(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            user.is_staff = False
            user.is_superuser = False
            user.is_active = True

            user.save()

            messages.success(request, "Đăng ký thành công, hãy đăng nhập")
            return redirect('login_cus')
    else:
        form = RegisterForm() #Nếu là GET hiển thị form trống

    return render(request, 'customers/register.html', {'form': form})

def login_customer(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:
                login(request, user)

                # Admin / staff
                if user.is_staff and user.is_superuser:
                    return redirect('dashboard')

                # Khách hàng
                return redirect('store_product_list')

            messages.error(request, 'Username hoặc mật khẩu không đúng')
    else:
        form = LoginForm()

    return render(request, 'customers/login.html', {'form': form})

def logout_customer(request):
    logout(request)
    return redirect('store_product_list')
