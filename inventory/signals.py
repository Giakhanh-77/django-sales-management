from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import SanPham
from .models import KhoHang

@receiver(post_save, sender=SanPham)
def dong_bo_san_pham_voi_kho(sender, instance, created, **kwargs):
    try:
        kho = instance.khohang
        if kho.ten_san_pham != instance.ten_san_pham:
            kho.ten_san_pham = instance.ten_san_pham
            kho.save(update_fields=['ten_san_pham'])
    except KhoHang.DoesNotExist:
        KhoHang.objects.create(
            san_pham=instance,
            ten_san_pham=instance.ten_san_pham,
            so_luong_ton=instance.so_luong_ton  
        )

@receiver(post_save, sender=KhoHang)
def dong_bo_kho_voi_san_pham(sender, instance, **kwargs):
    # Chỉ đồng bộ tên khi thay đổi
    san_pham = instance.san_pham
    if san_pham.ten_san_pham != instance.ten_san_pham:
        san_pham.ten_san_pham = instance.ten_san_pham
        san_pham.save(update_fields=['ten_san_pham'])
