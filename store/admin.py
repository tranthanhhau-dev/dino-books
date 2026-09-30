from django.contrib import admin
from django.utils.html import format_html
from .models import Category, AgeGroup, BookCondition, Book, Order, OrderItem, TradeInRequest, CustomerReview

admin.site.site_header = "Tiệm Sách Dino - Quản Trị Hệ Thống"
admin.site.site_title = "Quản lý Tiệm Sách Dino"
admin.site.index_title = "Bảng điều khiển Kho sách & Đơn hàng"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order', 'book_count']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = "Số lượng sách"


@admin.register(AgeGroup)
class AgeGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'badge_color', 'book_count']
    prepopulated_fields = {'slug': ('name',)}

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = "Số lượng sách"


@admin.register(BookCondition)
class BookConditionAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating_percentage', 'criteria', 'book_count']

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = "Số sách thuộc tình trạng này"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['thumbnail', 'title', 'price_display', 'original_price_display', 'discount_badge', 'condition', 'age_group', 'stock_status', 'is_featured', 'created_at']
    list_filter = ['category', 'age_group', 'condition', 'cover_type', 'is_featured', 'is_hot_deal']
    search_fields = ['title', 'vietnamese_title', 'author', 'publisher', 'isbn', 'series_name']
    list_editable = ['is_featured']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at', 'image_preview']
    save_on_top = True

    fieldsets = (
        ("Thông tin cơ bản", {
            "fields": ("title", "vietnamese_title", "slug", "author", "publisher", "series_name", "category", "age_group")
        }),
        ("Tình trạng sách cũ & Giá bán", {
            "fields": ("condition", "condition_detail", "original_price", "price", "stock")
        }),
        ("Thông số chi tiết", {
            "fields": ("reading_level", "cover_type", "pages", "publication_year", "isbn")
        }),
        ("Nội dung giới thiệu", {
            "fields": ("description",)
        }),
        ("Hình ảnh thực tế của sách", {
            "fields": ("cover_image", "image_preview", "extra_image_1", "extra_image_2", "extra_image_3", "image_url_fallback")
        }),
        ("Cấu hình hiển thị", {
            "fields": ("is_featured", "is_hot_deal", "views_count", "created_at", "updated_at")
        }),
    )

    def thumbnail(self, obj):
        url = obj.get_image_url()
        return format_html('<img src="{}" style="width: 50px; height: 65px; object-fit: cover; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);" />', url)
    thumbnail.short_description = "Ảnh bìa"

    def image_preview(self, obj):
        url = obj.get_image_url()
        return format_html('<img src="{}" style="max-height: 200px; border-radius: 8px;" />', url)
    image_preview.short_description = "Xem trước ảnh"

    def price_display(self, obj):
        return f"{obj.price:,.0f} đ"
    price_display.short_description = "Giá thanh lý"

    def original_price_display(self, obj):
        if obj.original_price:
            return f"{obj.original_price:,.0f} đ"
        return "-"
    original_price_display.short_description = "Giá bìa gốc"

    def discount_badge(self, obj):
        discount = obj.discount_percent
        if discount > 0:
            return format_html('<span style="background: #fee2e2; color: #dc2626; padding: 2px 8px; border-radius: 12px; font-weight: bold; font-size: 11px;">-{}%</span>', discount)
        return "-"
    discount_badge.short_description = "Tiết kiệm"

    def stock_status(self, obj):
        if obj.stock > 0:
            return format_html('<span style="background: #dcfce7; color: #166534; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 600;">Còn {} cuốn</span>', obj.stock)
        return format_html('<span style="background: #f1f5f9; color: #64748b; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Đã bán</span>')
    stock_status.short_description = "Kho hàng"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['book_title', 'price', 'quantity', 'line_total']

    def line_total(self, obj):
        return f"{obj.line_total:,.0f} đ"
    line_total.short_description = "Thành tiền"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_code', 'customer_name', 'customer_phone', 'total_display', 'payment_method_badge', 'payment_status_badge', 'status_badge', 'created_at']
    list_filter = ['status', 'payment_status', 'payment_method', 'created_at']
    search_fields = ['order_code', 'customer_name', 'customer_phone', 'shipping_address']
    list_editable = []
    inlines = [OrderItemInline]
    readonly_fields = ['order_code', 'created_at', 'updated_at']

    fieldsets = (
        ("Thông tin đơn hàng", {
            "fields": ("order_code", "status", "created_at", "updated_at")
        }),
        ("Thông tin khách hàng & Giao hàng", {
            "fields": ("customer_name", "customer_phone", "customer_email", "shipping_address", "city", "note", "tracking_number")
        }),
        ("Thanh toán", {
            "fields": ("payment_method", "payment_status", "subtotal", "shipping_fee", "total_amount")
        }),
    )

    def total_display(self, obj):
        return f"{obj.total_amount:,.0f} đ"
    total_display.short_description = "Tổng tiền"

    def payment_method_badge(self, obj):
        if obj.payment_method == 'cod':
            return "COD (Tiền mặt)"
        return obj.get_payment_method_display()
    payment_method_badge.short_description = "Hình thức TT"

    def payment_status_badge(self, obj):
        if obj.payment_status == 'paid':
            return format_html('<span style="background: #dcfce7; color: #166534; padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: 600;">Đã TT</span>')
        return format_html('<span style="background: #fef3c7; color: #b45309; padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: 600;">Chưa TT</span>')
    payment_status_badge.short_description = "TT Thanh toán"

    def status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'confirmed': '#3b82f6',
            'packing': '#8b5cf6',
            'shipping': '#06b6d4',
            'completed': '#10b981',
            'cancelled': '#ef4444',
        }
        color = colors.get(obj.status, '#64748b')
        return format_html(f'<span style="background: {color}20; color: {color}; border: 1px solid {color}40; padding: 3px 8px; border-radius: 10px; font-size: 11px; font-weight: 600;">{obj.get_status_display()}</span>')
    status_badge.short_description = "Trạng thái đơn"


@admin.register(TradeInRequest)
class TradeInRequestAdmin(admin.ModelAdmin):
    list_display = ['contact_name', 'phone', 'book_count', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['contact_name', 'phone', 'description']
    list_editable = ['status']


@admin.register(CustomerReview)
class CustomerReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'child_age', 'rating', 'book_bought', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved']
    list_editable = ['is_approved']
