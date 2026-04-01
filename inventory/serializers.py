from rest_framework import serializers
from .models import KhoHang

class KhoHangSerializer(serializers.ModelSerializer):
    ten_san_pham = serializers.CharField(source='san_pham.ten_san_pham', read_only=True)
    canh_bao = serializers.SerializerMethodField()

    class Meta:
        model = KhoHang
        fields = ['id', 'ten_san_pham', 'so_luong_ton', 'muc_canh_bao', 'canh_bao']
        read_only_fields = ['ten_san_pham', 'canh_bao']

    def get_canh_bao(self, obj):
        return "Cần nhập thêm hàng" if obj.so_luong_ton < obj.muc_canh_bao else "Đủ hàng"