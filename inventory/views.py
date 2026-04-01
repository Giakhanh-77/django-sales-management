from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from django.db.models import F
from .models import KhoHang
from .serializers import KhoHangSerializer


class IsStaffUser(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.is_staff
        )

@staff_member_required(login_url='login')
def inventory_list(request):
    return render(request, 'inventory/khohang.html')

class KhoHangViewSet(viewsets.ModelViewSet):
    queryset = KhoHang.objects.all().select_related('san_pham')
    serializer_class = KhoHangSerializer
    permission_classes = [IsStaffUser]

    @action(detail=False, methods=['get'])
    def canh_bao(self, request):
        #lọc hàng tồn kho thấp
        hang_thieu = self.queryset.filter(
            so_luong_ton__lt=F('muc_canh_bao') 
        )
        serializer = self.get_serializer(hang_thieu, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post']) #Tạo API custom cho danh sách
    def nhap_hang(self, request, pk=None):
        try:
            kho = self.get_object() #Lấy bản ghi kho theo id
            so_luong_nhap = int(request.data.get('so_luong_nhap', 0))

            if so_luong_nhap <= 0:
                return Response(
                    {"error": "Số lượng nhập phải > 0"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            kho.nhap_hang(so_luong_nhap)

            return Response({
                "message": f"✅ Đã nhập thêm {so_luong_nhap} sản phẩm.",
                "so_luong_ton": kho.so_luong_ton
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['post'])
    def xuat_hang(self, request, pk=None):
        try:
            kho = self.get_object()
            so_luong_xuat = int(request.data.get('so_luong_xuat', 0))

            if so_luong_xuat <= 0:
                return Response(
                    {"error": "Số lượng xuất phải > 0"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            kho.xuat_hang(so_luong_xuat)

            return Response({
                "message": f"🛒 Đã xuất {so_luong_xuat} sản phẩm.",
                "so_luong_ton": kho.so_luong_ton
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
