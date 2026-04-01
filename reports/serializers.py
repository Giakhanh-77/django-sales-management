from rest_framework import serializers
from products.models import SanPham

class DoanhThuSerializer(serializers.Serializer):
    ky = serializers.CharField()
    tong_doanh_thu = serializers.DecimalField(max_digits=15, decimal_places=2)

class SanPhamBanChaySerializer(serializers.ModelSerializer):
    hinh_anh = serializers.SerializerMethodField()

    class Meta:
        model = SanPham
        fields = ['ten_san_pham', 'so_luot_ban', 'hinh_anh']

    def get_hinh_anh(self, obj):
        request = self.context.get('request')
        if obj.hinh_anh:
            if request:
                return request.build_absolute_uri(obj.hinh_anh.url)
            return obj.hinh_anh.url
        return None