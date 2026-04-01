from django.apps import apps
from django.db import models
from django.db.models import Sum, F
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from django.db import transaction
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()
# Custom Manager: Thống kê doanh thu
class DonHangManager(models.Manager):
    def doanh_thu_theo_ngay(self):
        return (
            self.filter(trang_thai='DA')
            .annotate(ky=TruncDay('ngay_dat'))
            .values('ky')
            .annotate(tong_doanh_thu=Sum('tong_tien'))
            .order_by('ky')
        )

    def doanh_thu_theo_tuan(self):
        return (
            self.filter(trang_thai='DA')
            .annotate(ky=TruncWeek('ngay_dat'))
            .values('ky')
            .annotate(tong_doanh_thu=Sum('tong_tien'))
            .order_by('ky')
        )

    def doanh_thu_theo_thang(self):
        return (
            self.filter(trang_thai='DA')
            .annotate(ky=TruncMonth('ngay_dat'))
            .values('ky')
            .annotate(tong_doanh_thu=Sum('tong_tien'))
            .order_by('ky')
        )

class DonHang(models.Model):
    TRANG_THAI_CHOICES = [
        ('CHO', 'Chờ xử lý'),
        ('DANG', 'Đang giao'),
        ('DA', 'Đã giao'),
        ('HUY', 'Đã hủy'),
    ]

    khach_hang = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ngay_dat = models.DateTimeField(default=timezone.now)
    tong_tien = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    trang_thai = models.CharField(max_length=10, choices=TRANG_THAI_CHOICES, default='CHO')

    objects = DonHangManager()

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"

    def __str__(self):
        return f"Đơn hàng #{self.id} - {self.khach_hang.ten}"

    def cap_nhat_tong_tien(self):
        """Tự động tính tổng tiền dựa trên chi tiết đơn hàng"""
        tong = self.chi_tiets.aggregate(
            tong=Sum(F('so_luong') * F('don_gia'))
        )['tong'] or 0
        self.tong_tien = tong
        self.save(update_fields=['tong_tien'])



#Model: Chi tiết đơn hàng
class ChiTietDonHang(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE, related_name='chi_tiets')
    san_pham = models.ForeignKey('products.SanPham', on_delete=models.CASCADE)
    so_luong = models.IntegerField()
    don_gia = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    def __str__(self):
        return f"{self.san_pham.ten_san_pham} ({self.so_luong})"

    def thanh_tien(self):
        return self.so_luong * self.don_gia

    def save(self, *args, **kwargs):
        """Khi thêm chi tiết mới → cập nhật tổng tiền đơn hàng"""
        super().save(*args, **kwargs)
        self.don_hang.cap_nhat_tong_tien()

# Model: Lịch sử giao dịch
class LichSuGiaoDich(models.Model):
    don_hang = models.ForeignKey(DonHang, on_delete=models.CASCADE, related_name='lich_sus')
    trang_thai_cu = models.CharField(max_length=10, null=True, blank=True)
    trang_thai_moi = models.CharField(max_length=10)
    thoi_gian = models.DateTimeField(auto_now_add=True)
    ghi_chu = models.TextField(blank=True, null=True)
    nguoi_thay_doi = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Lịch sử giao dịch"
        verbose_name_plural = "Lịch sử giao dịch"

    def __str__(self):
        return f"Lịch sử #{self.id} - Đơn hàng {self.don_hang.id}"



@receiver(pre_save, sender=DonHang)
def luu_trang_thai_cu(sender, instance, **kwargs):
    """Ghi nhớ trạng thái cũ để so sánh khi lưu"""
    if instance.pk:
        try:
            instance._trang_thai_cu = DonHang.objects.get(pk=instance.pk).trang_thai
        except DonHang.DoesNotExist:
            instance._trang_thai_cu = None
    else:
        instance._trang_thai_cu = None


@receiver(post_save, sender=DonHang)
def cap_nhat_ton_va_lich_su(sender, instance, created, **kwargs):
    KhoHang = apps.get_model('inventory', 'KhoHang')
    SanPham = apps.get_model('products', 'SanPham')
    LichSuGiaoDich = apps.get_model('orders', 'LichSuGiaoDich')

    trang_thai_cu = getattr(instance, '_trang_thai_cu', None)
    trang_thai_moi = instance.trang_thai

    with transaction.atomic():
        # === Khi đơn chuyển sang “ĐÃ GIAO” ===
        if trang_thai_moi == 'DA' and trang_thai_cu != 'DA':
            tong_so_luong = 0

            for ct in instance.chi_tiets.select_related('san_pham'):
                kho = KhoHang.objects.select_for_update().get(san_pham=ct.san_pham)
                if kho.so_luong_ton < ct.so_luong:
                    raise ValueError(f"Tồn kho không đủ cho {ct.san_pham.ten_san_pham}")

                # Trừ tồn kho
                kho.so_luong_ton = F('so_luong_ton') - ct.so_luong
                kho.save(update_fields=['so_luong_ton'])

                # Đồng bộ về SanPham
                SanPham.objects.filter(pk=ct.san_pham.pk).update(
                    so_luong_ton=F('so_luong_ton') - ct.so_luong,
                    so_luot_ban=F('so_luot_ban') + ct.so_luong
                )

                tong_so_luong += ct.so_luong

            # Tăng lượt mua theo tổng số lượng trong đơn
            User.objects.filter(pk=instance.khach_hang.pk).update(
                so_luot_mua=F('so_luot_mua') + tong_so_luong
            )

        # === Khi đơn từ “ĐÃ GIAO” → “HỦY” ===
        elif trang_thai_cu == 'DA' and trang_thai_moi == 'HUY':
            tong_so_luong = 0

            for ct in instance.chi_tiets.select_related('san_pham'):
                kho = KhoHang.objects.select_for_update().get(san_pham=ct.san_pham)

                # Hoàn lại tồn kho
                kho.so_luong_ton = F('so_luong_ton') + ct.so_luong
                kho.save(update_fields=['so_luong_ton'])

                # Đồng bộ về SanPham
                SanPham.objects.filter(pk=ct.san_pham.pk).update(
                    so_luong_ton=F('so_luong_ton') + ct.so_luong,
                    so_luot_ban=F('so_luot_ban') - ct.so_luong
                )

                tong_so_luong += ct.so_luong

            # Giảm lượt mua tương ứng
            User.objects.filter(pk=instance.khach_hang.pk).update(
                so_luot_mua=F('so_luot_mua') - tong_so_luong
            )

        # === Ghi lịch sử thay đổi ===
        def tao_lich_su():
            if created:
                ghi_chu = f"Tạo đơn hàng #{instance.id} (Trạng thái: {trang_thai_moi})"
            else:
                ghi_chu = f"Đổi trạng thái từ {trang_thai_cu or 'None'} → {trang_thai_moi}"

            LichSuGiaoDich.objects.create(
                don_hang=instance,
                trang_thai_cu=trang_thai_cu,
                trang_thai_moi=trang_thai_moi,
                ghi_chu=ghi_chu,
                nguoi_thay_doi="Hệ thống"
            )

        transaction.on_commit(tao_lich_su)