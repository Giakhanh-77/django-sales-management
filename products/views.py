from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets, filters, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from .models import SanPham, DanhMuc
from .serializers import SanPhamSerializer, DanhMucSerializer
from .forms import SanPhamForm


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )

class DanhMucViewSet(viewsets.ModelViewSet):
    queryset = DanhMuc.objects.all()
    serializer_class = DanhMucSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['ten_danh_muc']
    permission_classes = [IsStaffUser]


class SanPhamViewSet(viewsets.ModelViewSet):
    queryset = SanPham.objects.select_related('danh_muc').all()
    serializer_class = SanPhamSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['ten_san_pham', 'ma_san_pham']
    ordering_fields = ['gia', 'ngay_tao']
    permission_classes = [IsStaffUser]

@staff_member_required(login_url='login')
def product_list(request):
    q = request.GET.get('q', '')
    danh_muc_id = request.GET.get('danh_muc', '')

    san_pham_list = SanPham.objects.all()
    if q:
        san_pham_list = san_pham_list.filter(ten_san_pham__icontains=q)
    if danh_muc_id:
        san_pham_list = san_pham_list.filter(danh_muc_id=danh_muc_id)

    danh_muc_list = DanhMuc.objects.all()
    form = SanPhamForm()

    return render(request, 'products/sanpham.html', {
        'san_pham_list': san_pham_list,
        'danh_muc_list': danh_muc_list,
        'form': form,
    })

@staff_member_required(login_url='login')
def product_add(request):
    if request.method == 'POST':
        form = SanPhamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Đã thêm sản phẩm mới!')
            return redirect('product_list')
    else:
        form = SanPhamForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Thêm sản phẩm'
    })

@staff_member_required(login_url='login')
def product_edit(request, id):
    sp = get_object_or_404(SanPham, id=id)

    if request.method == 'POST':
        form = SanPhamForm(request.POST, request.FILES, instance=sp)
        if form.is_valid():
            form.save()
            messages.success(request, '✏️ Cập nhật sản phẩm thành công!')
            return redirect('product_list')
    else:
        form = SanPhamForm(instance=sp)

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': 'Chỉnh sửa sản phẩm'
    })

@staff_member_required(login_url='login')
def product_delete(request, id):
    sp = get_object_or_404(SanPham, id=id)

    if request.method == 'POST':
        sp.delete()
        messages.success(request, '🗑️ Đã xóa sản phẩm!')
        return redirect('product_list')

    return render(request, 'products/product_confirm_delete.html', {'sp': sp})

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def top_products(request):
    top = (
        SanPham.objects
        .order_by('-so_luot_ban')[:5]
        .values('ten_san_pham', 'so_luot_ban', 'gia')
    )

    data = [
        {
            'ten_san_pham': sp['ten_san_pham'],
            'so_luot_ban': sp['so_luot_ban'],
            'doanh_thu': float(sp['gia']) * sp['so_luot_ban'],
        }
        for sp in top
    ]

    return Response(data)
