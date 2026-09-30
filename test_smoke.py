import os
import sys
import django

sys.stdout.reconfigure(encoding='utf-8')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiem_sach_bot.settings')
django.setup()

from django.test import Client
from store.models import Book, Order

client = Client()

print("1. Testing Home page...")
res = client.get('/')
assert res.status_code == 200, f"Home failed: {res.status_code}"
assert "Dino Books" in res.content.decode('utf-8')
print("-> Home OK")

print("2. Testing Catalog...")
res = client.get('/sach/')
assert res.status_code == 200, f"Catalog failed: {res.status_code}"
print("-> Catalog OK")

book = Book.objects.filter(stock__gt=0).first()
print(f"3. Testing Book Detail for '{book.title}'...")
res = client.get(f'/sach/{book.slug}/')
assert res.status_code == 200, f"Detail failed: {res.status_code}"
assert book.title in res.content.decode('utf-8')
print("-> Book detail OK")

print(f"4. Testing Add to Cart for book id {book.id}...")
res = client.get(f'/gio-hang/them/{book.id}/', follow=True)
assert res.status_code == 200
print("-> Add to Cart OK")

print("5. Testing Cart view...")
res = client.get('/gio-hang/')
assert res.status_code == 200
assert book.title in res.content.decode('utf-8')
print("-> Cart OK")

print("6. Testing Checkout GET...")
res = client.get('/thanh-toan/')
assert res.status_code == 200
print("-> Checkout GET OK")

print("7. Testing Checkout POST (COD order)...")
res = client.post('/thanh-toan/', {
    'customer_name': 'Mẹ Thùy Trang',
    'customer_phone': '0965112006',
    'customer_email': 'thuytrang@gmail.com',
    'city': 'Hà Nội',
    'shipping_address': 'Số 18 Hoàng Quốc Việt, Cầu Giấy',
    'note': 'Bọc góc sách giúp mình nhé',
    'payment_method': 'cod',
}, follow=True)
assert res.status_code == 200
assert "Đặt Hàng Thành Công" in res.content.decode('utf-8')
assert "Thanh toán khi nhận sách (COD)" in res.content.decode('utf-8')
assert "img.vietqr.io" not in res.content.decode('utf-8')
print("-> Checkout POST (COD) OK")

created_order = Order.objects.first()
print(f"8. Testing Order Tracking for order {created_order.order_code}...")
res = client.get(f'/tra-cuu-don-hang/?query={created_order.order_code}')
assert res.status_code == 200
assert created_order.customer_name in res.content.decode('utf-8')
print("-> Order tracking OK")

print("9. Testing Trade-in GET...")
res = client.get('/ky-gui-thanh-ly/')
assert res.status_code == 200
print("-> Trade-in GET OK")

print("10. Testing About page...")
res = client.get('/gioi-thieu/')
assert res.status_code == 200
print("-> About page OK")

print("ALL SMOKE TESTS PASSED PERFECTLY!")
