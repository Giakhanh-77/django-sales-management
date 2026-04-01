from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required  


def landing_view(request):
    return render(request, 'landing.html')
@login_required(login_url='login')  
def dashboard_view(request):
    return render(request, 'home.html')

#Trang đăng ký
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = request.POST.get('email', '').strip()
            if email:
                user.email = email
            user.save()
            messages.success(request, "🎉 Tạo tài khoản thành công! Vui lòng đăng nhập.")
            return redirect('login')
        else:
            messages.error(request, "❌ Đăng ký thất bại! Hãy kiểm tra lại thông tin.")
            print(form.errors)
    else:
        form = UserCreationForm()

    storage = messages.get_messages(request)
    for _ in storage:
        pass

    return render(request, 'users/dangky.html', {'form': form})


#Trang đăng nhập
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Đăng nhập thành công!")

            return redirect('dashboard') 
            
        else:
            messages.error(request, "Tên đăng nhập hoặc mật khẩu không đúng!")
    else:
        form = AuthenticationForm()
    return render(request, 'users/dangnhap.html', {'form': form})


#Đăng xuất
def logout_view(request):
    logout(request)
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    return redirect('landing')
