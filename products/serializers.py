from rest_framework import serializers
from .models import SanPham, DanhMuc

class DanhMucSerializer(serializers.ModelSerializer):
    class Meta:
        model = DanhMuc
        fields = ['id', 'ten_danh_muc', 'mo_ta']

class SanPhamSerializer(serializers.ModelSerializer):
    danh_muc = DanhMucSerializer(read_only=True)
    danh_muc_id = serializers.PrimaryKeyRelatedField(
        queryset=DanhMuc.objects.all(), source='danh_muc', write_only=True
    )

    class Meta:
        model = SanPham
        fields = [
            'id', 'ma_san_pham', 'ten_san_pham', 'danh_muc', 'danh_muc_id',
            'gia', 'mo_ta', 'hinh_anh', 'ngay_tao', 'so_luong_ton'
        ]
