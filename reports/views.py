from django.db.models import Sum, Count, F
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from customers.models import CustomUser
from inventory.models import KhoHang
from orders.models import DonHang, ChiTietDonHang
from products.models import SanPham
from django.shortcuts import render
from django.db.models.functions import TruncMonth, TruncDay, TruncWeek
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required(login_url='login')
def report_home(request):
    """Trang giao diện báo cáo tổng hợp (ADMIN)"""
    return render(request, 'reports/baocao.html')

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def sales_report(request):
    kieu = request.GET.get('kieu', 'thang')
    product_id = request.GET.get('product')
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')

    qs = DonHang.objects.filter(trang_thai='DA')

    if from_date:
        qs = qs.filter(ngay_dat__date__gte=from_date)
    if to_date:
        qs = qs.filter(ngay_dat__date__lte=to_date)

    if product_id:
        qs = qs.filter(chi_tiets__san_pham_id=product_id)

    if kieu == 'ngay':
        qs = qs.annotate(ky=TruncDay('ngay_dat'))
    elif kieu == 'tuan':
        qs = qs.annotate(ky=TruncWeek('ngay_dat'))
    else:
        qs = qs.annotate(ky=TruncMonth('ngay_dat'))

    data = (
        qs.values('ky')
        .annotate(
            doanh_thu=Sum('tong_tien'),
            so_don=Count('id', distinct=True),
            so_san_pham=Sum('chi_tiets__so_luong')
        )
        .order_by('ky')
    )

    return Response([
        {
            "key": d["ky"].strftime("%Y-%m-%d") if d["ky"] else "N/A",
            "doanh_thu": d["doanh_thu"] or 0,
            "so_don": d["so_don"] or 0,
            "so_san_pham": d["so_san_pham"] or 0,
        }
        for d in data
    ])


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def top_products_report(request):
    limit = int(request.GET.get('limit', 5))

    qs = (
        SanPham.objects
        .filter(so_luot_ban__gt=0)
        .annotate(value=F('so_luot_ban') * F('gia'))
        .order_by('-so_luot_ban')[:limit]
    )

    return Response([
        {
            "ten": sp.ten_san_pham,
            "value": sp.value,
            "qty": sp.so_luot_ban,
        }
        for sp in qs
    ])


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def doanh_thu_hom_nay(request):
    today = timezone.now().date()

    doanh_thu = (
        DonHang.objects
        .filter(trang_thai='DA', ngay_dat__date=today)
        .aggregate(tong=Sum('tong_tien'))['tong'] or 0
    )

    return Response({
        "ngay": today.strftime("%Y-%m-%d"),
        "doanh_thu_hom_nay": float(doanh_thu)
    })

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def tong_hang_da_ban(request):
    tong = (
        ChiTietDonHang.objects
        .filter(don_hang__trang_thai='DA')
        .aggregate(tong=Sum('so_luong'))['tong'] or 0
    )

    return Response({
        "tong_so_luong_da_ban": int(tong)
    })

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def stock_alerts(request):
    hang_thieu = (
        KhoHang.objects
        .filter(so_luong_ton__lt=F('muc_canh_bao'))
        .select_related('san_pham')
    )

    return Response([
        {
            "ten_san_pham": h.san_pham.ten_san_pham,
            "so_luong_ton": h.so_luong_ton,
            "muc_canh_bao": h.muc_canh_bao,
        }
        for h in hang_thieu
    ])

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def latest_customers(request):
    limit = int(request.GET.get('limit', 5))

    qs = CustomUser.objects.order_by('-ngay_tao')[:limit]

    return Response([
        {
            "ten": u.ten,
            "sdt": u.sdt,
            "ngay_tao": u.ngay_tao,
        }
        for u in qs
    ])

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def pending_orders(request):
    pending = DonHang.objects.filter(trang_thai='CHO').select_related('khach_hang')

    return Response([
        {
            "id": d.id,
            "khach_hang": d.khach_hang.ten,
            "sdt": d.khach_hang.sdt,
            "tong_tien": float(d.tong_tien),
            "ngay_dat": d.ngay_dat.strftime("%Y-%m-%d %H:%M:%S"),
            "trang_thai": d.get_trang_thai_display(),
        }
        for d in pending
    ])

@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def daily_revenue(request):
    data = (
        DonHang.objects
        .filter(trang_thai='DA')
        .annotate(ngay=TruncDay('ngay_dat'))
        .values('ngay')
        .annotate(total=Sum('tong_tien'))
        .order_by('ngay')
    )

    return Response([
        {
            "label": item['ngay'].strftime("%d/%m"),
            "value": float(item['total'] or 0)
        }
        for item in data
    ])
