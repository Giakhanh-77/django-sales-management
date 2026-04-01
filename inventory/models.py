from django.db import models

class KhoHang(models.Model):
    san_pham = models.OneToOneField(
        'products.SanPham',
        on_delete=models.CASCADE,
        related_name='khohang'
    )
    ten_san_pham = models.CharField(max_length=150, editable=False)
    so_luong_ton = models.IntegerField(default=0)
    muc_canh_bao = models.IntegerField(default=5)

    def canh_bao(self):
        """Kiểm tra nếu hàng tồn dưới mức cảnh báo"""
        return self.so_luong_ton < self.muc_canh_bao

    def nhap_hang(self, so_luong):
        """Cộng thêm hàng vào kho"""
        self.so_luong_ton += so_luong
        self.save()

    def xuat_hang(self, so_luong):
        """Trừ hàng khỏi kho"""
        if self.so_luong_ton >= so_luong:
            self.so_luong_ton -= so_luong
            self.save()
        else:
            raise ValueError("Không đủ hàng trong kho!")

    def save(self, *args, **kwargs):
        """Đồng bộ tên sản phẩm"""
        if self.san_pham:
            self.ten_san_pham = self.san_pham.ten_san_pham
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ten_san_pham} | Tồn: {self.so_luong_ton}"

