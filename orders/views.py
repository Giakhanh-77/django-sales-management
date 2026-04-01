from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission
from django.db import transaction
from .models import DonHang, ChiTietDonHang, LichSuGiaoDich
from .serializers import (
    DonHangSerializer,
    ChiTietDonHangSerializer,
    LichSuGiaoDichSerializer
)
from customers.models import CustomUser

class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )

class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.khach_hang == request.user

@staff_member_required(login_url='login')
def order_list(request):
    return render(request, 'orders/donhang.html')

class DonHangViewSet(viewsets.ModelViewSet):
    serializer_class = DonHangSerializer    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return DonHang.objects.all().order_by('-ngay_dat')

        return DonHang.objects.filter(
            khach_hang=user
        ).order_by('-ngay_dat')
    def get_permissions(self):
        if self.action in [
            'cap_nhat_trang_thai',
            'them_chi_tiet',
            'thong_ke',
            'lich_su'
        ]:
            permission_classes = [IsStaffUser]
        elif self.action in ['retrieve']:
            permission_classes = [IsOwnerOrStaff]
        else:
            permission_classes = [permissions.IsAuthenticated]

        return [p() for p in permission_classes]
    @action(detail=True, methods=['post'])
    @transaction.atomic
    def cap_nhat_trang_thai(self, request, pk=None):
        don_hang = self.get_object()
        trang_thai_moi = request.data.get('trang_thai')
        ghi_chu = request.data.get('ghi_chu', '')

        if trang_thai_moi not in dict(DonHang.TRANG_THAI_CHOICES):
            return Response(
                {'error': 'Trạng thái không hợp lệ.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        don_hang.trang_thai = trang_thai_moi
        don_hang.save()

        return Response({
            'message': f'Đơn hàng #{don_hang.id} đã chuyển sang {trang_thai_moi}.'
        })
    @action(detail=True, methods=['post'])
    def them_chi_tiet(self, request, pk=None):
        don_hang = self.get_object()
        data = request.data.copy()
        data['don_hang'] = don_hang.id

        serializer = ChiTietDonHangSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Đã thêm sản phẩm và cập nhật tổng tiền.'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @action(detail=False, methods=['post'])
    @transaction.atomic
    def tao_don_hang_day_du(self, request):
        from products.models import SanPham

        try:
            san_pham_id = request.data.get("san_pham")
            so_luong = int(request.data.get("so_luong", 1))
            khach_hang_id = request.data.get("khach_hang")

            if not san_pham_id:
                return Response(
                    {"error": "Thiếu sản phẩm."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            san_pham = SanPham.objects.get(pk=san_pham_id)
            khach_hang = CustomUser.objects.get(pk=khach_hang_id)

            don = DonHang.objects.create(
                khach_hang=khach_hang,
                trang_thai="CHO"
            )

            ChiTietDonHang.objects.create(
                don_hang=don,
                san_pham=san_pham,
                so_luong=so_luong,
                don_gia=san_pham.gia
            )

            don.cap_nhat_tong_tien()

            return Response({
                "message": f"✅ Đã tạo đơn hàng #{don.id} thành công!",
                "id": don.id
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    @action(detail=False, methods=['get'])
    def thong_ke(self, request):
        kieu = request.query_params.get('kieu', 'ngay')

        if kieu == 'tuan':
            data = DonHang.objects.doanh_thu_theo_tuan()
        elif kieu == 'thang':
            data = DonHang.objects.doanh_thu_theo_thang()
        else:
            data = DonHang.objects.doanh_thu_theo_ngay()

        return Response(data)
    @action(detail=True, methods=['get'])
    def lich_su(self, request, pk=None):
        don_hang = self.get_object()
        lich_su = LichSuGiaoDich.objects.filter(don_hang=don_hang)
        serializer = LichSuGiaoDichSerializer(lich_su, many=True)
        return Response(serializer.data)
class LichSuGiaoDichViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        LichSuGiaoDich.objects
        .select_related('don_hang')
        .all()
        .order_by('-thoi_gian')
    )
    serializer_class = LichSuGiaoDichSerializer
    permission_classes = [IsStaffUser]
