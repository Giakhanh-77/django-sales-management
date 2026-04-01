from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from products.models import SanPham, DanhMuc
from orders.models import DonHang, ChiTietDonHang


def _get_cart(request):
    return request.session.setdefault('cart', {})

def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def buy_now(request, ma_san_pham):
    product = get_object_or_404(SanPham, ma_san_pham=ma_san_pham)

    cart = _get_cart(request)
    cart[str(product.ma_san_pham)] = cart.get(str(product.ma_san_pham), 0) + 1
    _save_cart(request, cart)

    messages.success(request, f"Đã thêm 1 x {product.ten_san_pham} vào giỏ hàng.")
    return redirect('store_cart')


def product_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category')

    products = SanPham.objects.all()

    if query:
        products = products.filter(ten_san_pham__icontains=query)

    if category_id:
        products = products.filter(danh_muc_id=category_id)

    best_sellers = SanPham.objects.order_by('-so_luot_ban')[:3]

    return render(request, 'buystore/product_list.html', {
        'products': products,
        'query': query,
        'selected_category': int(category_id) if category_id else None,
        'best_sellers': best_sellers
    })

def product_detail(request, ma_san_pham):
    product = get_object_or_404(SanPham, ma_san_pham=ma_san_pham)

    if request.method == 'POST':
        qty = int(request.POST.get('qty', 1))
        action = request.POST.get('action')  

        cart = _get_cart(request)
        sku = str(product.ma_san_pham)

        cart[sku] = cart.get(sku, 0) + qty
        _save_cart(request, cart)

        if action == 'buy':
            return redirect('store_cart')

        messages.success(
            request,
            f"Đã thêm {qty} x {product.ten_san_pham} vào giỏ hàng."
        )
        return redirect(request.path)

    return render(request, 'buystore/product_detail.html', {
        'product': product
    })


def cart_view(request):
    cart = _get_cart(request)
    items = []
    total = Decimal('0')

    for sku, qty in cart.items():
        try:
            sp = SanPham.objects.get(ma_san_pham=sku)
            line_total = sp.gia * qty
            total += line_total
            items.append({'product': sp, 'qty': qty, 'line_total': line_total})
        except SanPham.DoesNotExist:
            continue

    return render(request, 'buystore/cart.html', {'items': items, 'total': total})


@require_POST
def update_cart(request):
    cart = _get_cart(request)
    action = request.POST.get('action')
    sku = request.POST.get('sku')

    if action == 'remove' and sku in cart:
        del cart[sku]

    elif action == 'update' and sku:
        qty = int(request.POST.get('qty', 0))
        if qty <= 0:
            cart.pop(sku, None)
        else:
            cart[sku] = qty

    total = Decimal('0')
    for skey, qty in cart.items():
        try:
            sp = SanPham.objects.get(ma_san_pham=skey)
            total += sp.gia * qty
        except SanPham.DoesNotExist:
            continue

    _save_cart(request, cart)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'total': int(total)})

    return redirect('store_cart')


def product_by_category(request, category_id): 
    category = get_object_or_404(DanhMuc, id=category_id) 
    products = SanPham.objects.filter(danh_muc=category) 
    return render(request, 'buystore/product_list.html', 
                  { 'products': products, 'query': "", 'selected_category': category })

@transaction.atomic #Đảm bảo an toàn dữ liệu
@login_required
def checkout(request):
    ORDER_STATUS = 'CHO'
    kh = request.user  
    cart = _get_cart(request)

    if not cart:
        messages.warning(request, "Giỏ hàng rỗng.")
        return redirect('store_product_list')

    if request.method == 'POST' and request.POST.get('action') == 'update_info':
        kh.ten = request.POST.get('new_name')
        kh.sdt = request.POST.get('new_phone')
        kh.dia_chi = request.POST.get('new_address')
        kh.save()

        messages.success(request, "Đã cập nhật thông tin giao hàng.")
        return redirect('store_checkout')

    if request.method == 'POST' and request.POST.get('action') == 'place_order':
        total = Decimal('0')
        total_qty = 0
        products_to_update = {}

        for sku, qty in cart.items():
            sp = SanPham.objects.select_for_update().get(ma_san_pham=sku)
            if sp.so_luong_ton < qty:
                messages.error(request, f"{sp.ten_san_pham} chỉ còn {sp.so_luong_ton}.")
                return redirect('store_cart')

            total += sp.gia * qty
            total_qty += qty
            products_to_update[sp] = qty

        order = DonHang.objects.create(
            khach_hang=kh,
            ngay_dat=timezone.now(),
            trang_thai=ORDER_STATUS,
            tong_tien=total
        )

        for sp, qty in products_to_update.items():
            ChiTietDonHang.objects.create(
                don_hang=order,
                san_pham=sp,
                so_luong=qty,
                don_gia=sp.gia
            )

        # kh.so_luot_mua += total_qty
        # kh.save()

        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, f"Đặt hàng thành công! Mã đơn #{order.id}")
        return redirect('store_product_list')

    items = []
    total = Decimal('0')
    for sku, qty in cart.items():
        sp = SanPham.objects.get(ma_san_pham=sku)
        items.append({
            'product': sp,
            'qty': qty,
            'line_total': sp.gia * qty
        })
        total += sp.gia * qty

    return render(request, 'buystore/checkout.html', {
        'items': items,
        'total': total,
        'kh': kh
    })



@login_required
def order_history(request):
    orders = DonHang.objects.filter(khach_hang=request.user).order_by('-ngay_dat')
    return render(request, 'buystore/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(DonHang, id=order_id, khach_hang=request.user)

    items = []
    for item in ChiTietDonHang.objects.filter(don_hang=order):
        items.append({
            'product': item.san_pham,
            'qty': item.so_luong,
            'price': item.don_gia,
            'line_total': item.don_gia * item.so_luong
        })

    return render(request, 'buystore/order_detail.html', {
        'order': order,
        'items': items
    })


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(DonHang, id=order_id, khach_hang=request.user)

    if order.trang_thai != 'CHO':
        messages.error(request, "Không thể hủy đơn đã xử lý.")
        return redirect('store_order_history')

    order.trang_thai = 'HUY'
    order.save()

    for item in ChiTietDonHang.objects.filter(don_hang=order):
        sp = item.san_pham
        sp.so_luong_ton += item.so_luong
        sp.save()

    messages.success(request, f"Đã hủy đơn #{order.id}.")
    return redirect('store_order_history')

