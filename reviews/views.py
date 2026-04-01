from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Review
from .services import can_review
from products.models import SanPham


# Đánh giá khách hàng
@login_required
def add_review(request, ma_san_pham):
    product = get_object_or_404(SanPham, ma_san_pham=ma_san_pham)

    if not can_review(request.user, product):
        messages.error(request, "Bạn chỉ có thể đánh giá sản phẩm đã mua.")
        return redirect('store_product_detail', ma_san_pham=ma_san_pham)

    if request.method == 'POST':
        Review.objects.update_or_create(
            san_pham=product,
            khach_hang=request.user,
            defaults={
                'so_sao': int(request.POST.get('rating')),
                'noi_dung': request.POST.get('comment')
            }
        )
        messages.success(request, "Cảm ơn bạn đã đánh giá!")

    return redirect('store_product_detail', ma_san_pham=ma_san_pham)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_reviews_preview(request):
    reviews = Review.objects.select_related(
        'khach_hang', 'san_pham'
    ).order_by('-ngay_tao')[:5]  

    return Response([
        {
            'khach_hang': r.khach_hang.ten,
            'san_pham': r.san_pham.ten_san_pham,
            'so_sao': r.so_sao,
            'noi_dung': (
                r.noi_dung[:80] + "..."
                if len(r.noi_dung) > 80 else r.noi_dung
            ),
            'ngay_tao': r.ngay_tao.isoformat()
        }
        for r in reviews
    ])



@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_reviews_all(request):
    reviews = Review.objects.select_related(
        'khach_hang', 'san_pham'
    ).order_by('-ngay_tao')

    return Response([
        {
            'khach_hang': r.khach_hang.ten,
            'san_pham': r.san_pham.ten_san_pham,
            'so_sao': r.so_sao,
            'noi_dung': r.noi_dung,
            'ngay_tao': r.ngay_tao.isoformat()
        }
        for r in reviews
    ])

@login_required
def admin_reviews_page(request):
    return render(request, 'reviews/admin_reviews.html')