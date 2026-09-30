from django.db import models
from django.utils.text import slugify
import uuid

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Tên thể loại")
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Mô tả thể loại")
    icon = models.CharField(max_length=50, default="book-open", help_text="Tên Lucide icon hoặc emoji")
    badge_bg = models.CharField(max_length=30, default="bg-amber-100 text-amber-800")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị")

    class Meta:
        verbose_name = "Thể loại sách"
        verbose_name_plural = "Thể loại sách"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug:
                self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AgeGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nhóm độ tuổi") # vd: "0 - 3 tuổi (Baby/Toddler)"
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.CharField(max_length=255, blank=True, verbose_name="Đặc điểm đọc")
    badge_color = models.CharField(max_length=50, default="bg-blue-100 text-blue-800", help_text="Class CSS Tailwind")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Nhóm tuổi"
        verbose_name_plural = "Nhóm tuổi"
        ordering = ['order', 'id']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            if not self.slug:
                self.slug = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BookCondition(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên tình trạng") # vd: "Mới 98% (Like New)"
    rating_percentage = models.PositiveIntegerField(default=90, verbose_name="Độ mới (%)")
    badge_color = models.CharField(max_length=50, default="bg-emerald-100 text-emerald-800")
    criteria = models.CharField(max_length=255, verbose_name="Tiêu chuẩn đánh giá", blank=True,
                                help_text="Vd: Gáy nguyên vẹn, ruột sách sạch tinh, không quăn gập mép")

    class Meta:
        verbose_name = "Tình trạng sách cũ"
        verbose_name_plural = "Tình trạng sách cũ"
        ordering = ['-rating_percentage']

    def __str__(self):
        return f"{self.name} ({self.rating_percentage}%)"


class Book(models.Model):
    COVER_CHOICES = [
        ('paperback', 'Bìa mềm (Paperback)'),
        ('hardcover', 'Bìa cứng (Hardcover)'),
        ('board_book', 'Bìa bồi cứng (Board Book cho bé)'),
        ('flap_sound', 'Sách tương tác / Lật mở / Âm thanh'),
    ]

    title = models.CharField(max_length=255, verbose_name="Tên sách (Tiếng Anh)")
    vietnamese_title = models.CharField(max_length=255, blank=True, verbose_name="Tên tiếng Việt / Giới thiệu nhanh")
    slug = models.SlugField(max_length=280, unique=True, blank=True)
    author = models.CharField(max_length=200, verbose_name="Tác giả")
    publisher = models.CharField(max_length=150, blank=True, verbose_name="Nhà xuất bản",
                                 help_text="Usborne, Scholastic, Penguin, Oxford, HarperCollins...")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books", verbose_name="Thể loại")
    age_group = models.ForeignKey(AgeGroup, on_delete=models.SET_NULL, null=True, related_name="books", verbose_name="Độ tuổi")
    condition = models.ForeignKey(BookCondition, on_delete=models.SET_NULL, null=True, related_name="books", verbose_name="Tình trạng")
    condition_detail = models.CharField(max_length=300, blank=True, verbose_name="Chi tiết thực tế cuốn sách này",
                                        help_text="Vd: Gáy chắc chắn, trang giấy đẹp tinh tươm, không ghi chú viết vẽ")
    
    original_price = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Giá bìa gốc (VNĐ)")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá bán thanh lý (VNĐ)")
    stock = models.PositiveIntegerField(default=1, verbose_name="Số lượng trong kho (Thường là 1)")
    
    reading_level = models.CharField(max_length=100, blank=True, verbose_name="Trình độ đọc",
                                     help_text="Vd: Phonics Stage 2, Lexile 520L, AR 3.4, Grade 3-5...")
    pages = models.PositiveIntegerField(null=True, blank=True, verbose_name="Số trang")
    cover_type = models.CharField(max_length=30, choices=COVER_CHOICES, default='paperback', verbose_name="Loại bìa")
    publication_year = models.PositiveIntegerField(null=True, blank=True, verbose_name="Năm xuất bản")
    series_name = models.CharField(max_length=150, blank=True, verbose_name="Thuộc bộ sách / Series (nếu có)")
    isbn = models.CharField(max_length=50, blank=True, verbose_name="Mã ISBN")
    
    description = models.TextField(verbose_name="Mô tả & Tóm tắt nội dung cuốn sách")
    
    cover_image = models.ImageField(upload_to="books/covers/", blank=True, null=True, verbose_name="Ảnh bìa thực tế")
    extra_image_1 = models.ImageField(upload_to="books/extras/", blank=True, null=True, verbose_name="Ảnh mặt sau / gáy")
    extra_image_2 = models.ImageField(upload_to="books/extras/", blank=True, null=True, verbose_name="Ảnh trang ruột 1")
    extra_image_3 = models.ImageField(upload_to="books/extras/", blank=True, null=True, verbose_name="Ảnh trang ruột 2")

    image_url_fallback = models.URLField(max_length=500, blank=True, verbose_name="Link ảnh ngoài (dự phòng)")

    is_featured = models.BooleanField(default=False, verbose_name="Sách nổi bật trang chủ")
    is_hot_deal = models.BooleanField(default=False, verbose_name="Giá hời hôm nay")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Lượt xem")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày thêm")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Sách tiếng Anh cũ"
        verbose_name_plural = "Kho Sách tiếng Anh cũ"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or f"book-{str(uuid.uuid4())[:8]}"
            slug = base_slug
            counter = 1
            while Book.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            diff = self.original_price - self.price
            return int(round((diff / self.original_price) * 100))
        return 0

    @property
    def is_in_stock(self):
        return self.stock > 0

    def get_image_url(self):
        if self.cover_image:
            return self.cover_image.url
        if self.image_url_fallback:
            return self.image_url_fallback
        return "/static/images/default-book.png"

    def __str__(self):
        return f"{self.title} ({self.price:,.0f}đ) - {self.condition}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('packing', 'Đang gói sách'),
        ('shipping', 'Đang giao hàng'),
        ('completed', 'Giao thành công'),
        ('cancelled', 'Đã hủy'),
    ]

    PAYMENT_CHOICES = [
        ('cod', 'Thanh toán tiền mặt khi nhận sách (COD)'),
        ('vietqr', 'Chuyển khoản (Đơn cũ)'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Chưa thanh toán'),
        ('paid', 'Đã thanh toán'),
    ]

    order_code = models.CharField(max_length=30, unique=True, verbose_name="Mã đơn hàng")
    customer_name = models.CharField(max_length=150, verbose_name="Họ tên phụ huynh / người nhận")
    customer_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    customer_email = models.EmailField(blank=True, verbose_name="Email nhận thông báo")
    shipping_address = models.CharField(max_length=255, verbose_name="Địa chỉ nhận hàng (Số nhà, đường)")
    city = models.CharField(max_length=100, verbose_name="Tỉnh / Thành phố")
    note = models.TextField(blank=True, verbose_name="Ghi chú đơn hàng")
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cod', verbose_name="Phương thức thanh toán")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid', verbose_name="Trạng thái thanh toán")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái đơn hàng")
    
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=0, default=25000, verbose_name="Phí ship")
    subtotal = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Tiền sách")
    total_amount = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Tổng thanh toán")

    tracking_number = models.CharField(max_length=100, blank=True, verbose_name="Mã vận đơn bưu cục")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian đặt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Cập nhật lần cuối")

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Quản lý Đơn hàng"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_code:
            import datetime
            today_str = datetime.date.today().strftime("%y%m%d")
            random_part = str(uuid.uuid4().hex)[:4].upper()
            self.order_code = f"DINO-{today_str}-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"#{self.order_code} - {self.customer_name} ({self.total_amount:,.0f}đ)"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Đơn hàng")
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, verbose_name="Sách")
    book_title = models.CharField(max_length=255, verbose_name="Tên sách lúc đặt")
    price = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Đơn giá")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")

    class Meta:
        verbose_name = "Chi tiết đơn hàng"
        verbose_name_plural = "Chi tiết đơn hàng"

    @property
    def line_total(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.book_title} x {self.quantity}"


class TradeInRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Mới gửi'),
        ('contacted', 'Đã liên hệ báo giá'),
        ('received', 'Đã nhận sách kiểm tra'),
        ('paid', 'Đã thanh toán / Ký gửi xong'),
        ('declined', 'Từ chối'),
    ]

    contact_name = models.CharField(max_length=150, verbose_name="Tên ba/mẹ")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại / Zalo")
    book_count = models.PositiveIntegerField(default=5, verbose_name="Ước tính số lượng cuốn")
    description = models.TextField(verbose_name="Danh sách hoặc thể loại sách muốn thanh lý/ký gửi",
                                  help_text="Vd: Khoảng 20 cuốn truyện tranh Scholastic, Usborne cho bé 5 tuổi, còn mới 90%...")
    photo = models.ImageField(upload_to="tradein/", blank=True, null=True, verbose_name="Ảnh chụp chồng sách")
    address = models.CharField(max_length=255, blank=True, verbose_name="Địa chỉ lấy sách (nếu có)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Trạng thái")
    admin_notes = models.TextField(blank=True, verbose_name="Ghi chú của tiệm")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày gửi yêu cầu")

    class Meta:
        verbose_name = "Yêu cầu ký gửi / Thanh lý sách"
        verbose_name_plural = "Ký gửi / Thanh lý sách cũ"
        ordering = ['-created_at']

    def __str__(self):
        return f"Ký gửi {self.book_count} cuốn - {self.contact_name} ({self.phone})"


class CustomerReview(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Tên phụ huynh")
    child_age = models.CharField(max_length=50, blank=True, verbose_name="Bé mấy tuổi")
    rating = models.PositiveIntegerField(default=5, verbose_name="Số sao (1-5)")
    comment = models.TextField(verbose_name="Đánh giá về sách và dịch vụ")
    book_bought = models.CharField(max_length=200, blank=True, verbose_name="Cuốn sách đã mua")
    is_approved = models.BooleanField(default=True, verbose_name="Hiển thị trên web")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Đánh giá của khách"
        verbose_name_plural = "Đánh giá của khách"

    def __str__(self):
        return f"{self.customer_name} ({self.rating} sao)"
