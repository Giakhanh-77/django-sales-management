from rest_framework import serializers
from .models import DonHang, ChiTietDonHang, LichSuGiaoDich


class ChiTietDonHangSerializer(serializers.ModelSerializer):
    ten_san_pham = serializers.CharField(source='san_pham.ten_san_pham', read_only=True)

    class Meta:
        model = ChiTietDonHang
        fields = ['id', 'don_hang', 'san_pham', 'ten_san_pham', 'so_luong', 'don_gia', 'thanh_tien']
        read_only_fields = ['thanh_tien']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['thanh_tien'] = instance.thanh_tien()
        return rep


class DonHangSerializer(serializers.ModelSerializer):
    chi_tiets = ChiTietDonHangSerializer(many=True, read_only=True)
    khach_hang_ten = serializers.CharField(source='khach_hang.ten', read_only=True)

    class Meta:
        model = DonHang
        fields = '__all__'
        read_only_fields = ['ngay_dat']  

class LichSuGiaoDichSerializer(serializers.ModelSerializer):
    ma_san_pham = serializers.SerializerMethodField()

    class Meta:
        model = LichSuGiaoDich
        fields = ['id', 'don_hang', 'trang_thai_cu', 'trang_thai_moi', 'thoi_gian',
                  'ghi_chu', 'ma_san_pham', 'nguoi_thay_doi']

    def get_ma_san_pham(self, obj):
        return [ct.san_pham.ma_san_pham for ct in obj.don_hang.chi_tiets.all()]