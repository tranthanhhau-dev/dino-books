from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('sach/', views.book_list_view, name='book_list'),
    path('sach/<slug:slug>/', views.book_detail_view, name='book_detail'),
    path('gio-hang/', views.cart_view, name='cart'),
    path('gio-hang/them/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('gio-hang/cap-nhat/<int:book_id>/', views.update_cart, name='update_cart'),
    path('gio-hang/xoa/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('thanh-toan/', views.checkout_view, name='checkout'),
    path('dat-hang-thanh-cong/<str:order_code>/', views.order_success_view, name='order_success'),
    path('tra-cuu-don-hang/', views.order_tracking_view, name='order_tracking'),
    path('ky-gui-thanh-ly/', views.trade_in_view, name='trade_in'),
    path('gioi-thieu/', views.about_view, name='about'),
    path('quan-ly-don-hang/', views.shop_orders_dashboard, name='orders_dashboard'),
    path('manifest.json', views.manifest_view, name='manifest'),
    path('sw.js', views.service_worker_view, name='service_worker'),
]

