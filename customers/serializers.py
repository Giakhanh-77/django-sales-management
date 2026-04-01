from rest_framework import serializers
from .models import CustomUser

class KhachHangSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "ten",
            "sdt",
            "email",
            "dia_chi",
            "so_luot_mua",
            "ngay_tao"
        ]