from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    ten = models.CharField(max_length=100)
    sdt = models.CharField(max_length=15, unique=True)
    dia_chi = models.TextField()
    so_luot_mua = models.IntegerField(default=0)
    ngay_tao = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"

    def __str__(self):
        return f"{self.ten} - {self.sdt}"