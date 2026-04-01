from products.models import SanPham

def best_sellers(request):
    return {
        'best_sellers': SanPham.objects.order_by('-so_luot_ban')[:5]
    }