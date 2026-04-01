from django import forms
from .models import SanPham

class SanPhamForm(forms.ModelForm):
    class Meta:
        model = SanPham
        fields = ['ma_san_pham', 'ten_san_pham', 'gia', 'so_luong_ton', 'mo_ta', 'hinh_anh', 'danh_muc']
        widgets = {
            'mo_ta': forms.Textarea(attrs={'rows': 3}),
        }
