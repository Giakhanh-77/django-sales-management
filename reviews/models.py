from django.db import models
from django.conf import settings
from products.models import SanPham
from django.utils import timezone

class Review(models.Model):
    san_pham = models.ForeignKey(
        SanPham,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    khach_hang = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    so_sao = models.PositiveSmallIntegerField()
    noi_dung = models.TextField()
    ngay_tao = models.DateTimeField(default=timezone.now)
    da_duyet = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        ordering = ['-ngay_tao']
        unique_together = ('san_pham', 'khach_hang')

    def __str__(self):
        return f"{self.san_pham} - {self.so_sao}⭐"