from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import SanPham
from inventory.models import KhoHang

#  Tự tạo hoặc đồng bộ số lượng tồn khi sản phẩm được lưu
@receiver(post_save, sender=SanPham)
def dong_bo_tu_sanpham(sender, instance, **kwargs):
    try:
        kho, created = KhoHang.objects.get_or_create(san_pham=instance)
        if kho.so_luong_ton != instance.so_luong_ton:
            kho.so_luong_ton = instance.so_luong_ton
            kho.save(update_fields=['so_luong_ton'])
    except Exception as e:
        print("❌ Lỗi khi đồng bộ kho:", e)


#  Xóa kho khi sản phẩm bị xóa (phòng trường hợp on_delete chưa hoạt động)
@receiver(post_delete, sender=SanPham)
def xoa_kho_khi_xoa_sanpham(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'khohang'):
            instance.khohang.delete()
    except Exception as e:
        print("⚠️ Không thể xóa kho tương ứng:", e)
