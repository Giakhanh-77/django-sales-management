from django.db import models
from django.utils import timezone

class DanhMuc(models.Model):
    ten_danh_muc = models.CharField(max_length=100, unique=True)
    mo_ta = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.ten_danh_muc


class SanPham(models.Model):
    ma_san_pham = models.CharField(max_length=20, unique=True)
    ten_san_pham = models.CharField(max_length=150)
    danh_muc = models.ForeignKey('DanhMuc', on_delete=models.SET_NULL, null=True)
    gia = models.DecimalField(max_digits=12, decimal_places=2)
    mo_ta = models.TextField(blank=True, null=True)
    so_luot_ban = models.IntegerField(default=0)
    hinh_anh = models.ImageField(upload_to='sanpham/', blank=True, null=True)
    so_luong_ton = models.IntegerField(default=0)
    ngay_tao = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.ten_san_pham