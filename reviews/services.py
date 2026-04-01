from orders.models import ChiTietDonHang

def can_review(user, product):
    return ChiTietDonHang.objects.filter(
        don_hang__khach_hang=user,
        san_pham=product,
        don_hang__trang_thai='DA'
    ).exists()