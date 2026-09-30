from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Category, AgeGroup, BookCondition, Book, Order, OrderItem, TradeInRequest, CustomerReview
from .utils import send_order_notification_email


def home_view(request):
    """
    Trang chủ Dino Books
    """
    featured_books = Book.objects.filter(is_featured=True, stock__gt=0)[:8]
    hot_deals = Book.objects.filter(is_hot_deal=True, stock__gt=0)[:6]
    latest_books = Book.objects.filter(stock__gt=0).order_by('-created_at')[:10]
    categories = Category.objects.all().order_by('order')[:8]
    age_groups = AgeGroup.objects.all().order_by('order')
    reviews = CustomerReview.objects.filter(is_approved=True).order_by('-created_at')[:6]

    context = {
        'featured_books': featured_books,
        'hot_deals': hot_deals,
        'latest_books': latest_books,
        'categories': categories,
        'age_groups': age_groups,
        'reviews': reviews,
    }
    return render(request, 'store/home.html', context)


def book_list_view(request):
    """
    Trang danh mục sách với bộ lọc đa tiêu chí (Thể loại, Độ tuổi, Độ mới, Giá bán)
    """
    books = Book.objects.all()

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        books = books.filter(
            Q(title__icontains=q) |
            Q(vietnamese_title__icontains=q) |
            Q(author__icontains=q) |
            Q(publisher__icontains=q) |
            Q(series_name__icontains=q) |
            Q(isbn__icontains=q)
        )

    # Category filter
    category_slug = request.GET.get('category', '')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=selected_category)

    # Age group filter
    age_slug = request.GET.get('age', '')
    selected_age = None
    if age_slug:
        selected_age = get_object_or_404(AgeGroup, slug=age_slug)
        books = books.filter(age_group=selected_age)

    # Condition filter
    condition_id = request.GET.get('condition', '')
    if condition_id:
        books = books.filter(condition_id=condition_id)

    # Cover type filter
    cover_type = request.GET.get('cover', '')
    if cover_type:
        books = books.filter(cover_type=cover_type)

    # Price range filter
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price and min_price.isdigit():
        books = books.filter(price__gte=int(min_price))
    if max_price and max_price.isdigit():
        books = books.filter(price__lte=int(max_price))

    # Stock filter (mặc định chỉ hiện sách còn hàng trừ khi có tuỳ chọn xem tất cả)
    show_all = request.GET.get('show_all', '')
    if not show_all:
        books = books.filter(stock__gt=0)

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price_asc':
        books = books.order_by('price')
    elif sort_by == 'price_desc':
        books = books.order_by('-price')
    elif sort_by == 'condition':
        books = books.order_by('-condition__rating_percentage')
    elif sort_by == 'views':
        books = books.order_by('-views_count')
    else:
        books = books.order_by('-created_at')

    # Pagination: 12 cuốn / trang
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,
        'total_count': books.count(),
        'selected_category': selected_category,
        'selected_age': selected_age,
        'current_q': q,
        'current_sort': sort_by,
        'current_condition': condition_id,
        'current_cover': cover_type,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'show_all': show_all,
    }
    return render(request, 'store/book_list.html', context)


def book_detail_view(request, slug):
    """
    Trang chi tiết sách, hình ảnh thực tế, thông số tình trạng
    """
    book = get_object_or_404(Book, slug=slug)
    
    # Tăng lượt xem
    Book.objects.filter(pk=book.pk).update(views_count=book.views_count + 1)
    
    # Sách tương tự cùng thể loại hoặc cùng độ tuổi
    related_books = Book.objects.filter(
        Q(category=book.category) | Q(age_group=book.age_group)
    ).exclude(pk=book.pk).filter(stock__gt=0)[:4]

    context = {
        'book': book,
        'related_books': related_books,
    }
    return render(request, 'store/book_detail.html', context)


# ==================== GIỎ HÀNG (SESSION CART) ====================

def cart_view(request):
    """
    Trang hiển thị giỏ hàng
    """
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = 0

    for book_id, item in cart.items():
        try:
            book = Book.objects.get(id=book_id)
            quantity = item.get('quantity', 1)
            line_total = book.price * quantity
            subtotal += line_total
            cart_items.append({
                'book': book,
                'quantity': quantity,
                'line_total': line_total,
            })
        except Book.DoesNotExist:
            continue

    # Miễn phí ship từ 250k
    shipping_fee = 0 if subtotal >= 250000 or subtotal == 0 else 25000
    total = subtotal + shipping_fee

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total': total,
        'free_shipping_threshold': 250000,
        'amount_needed_for_free_ship': max(0, 250000 - subtotal),
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, book_id):
    """
    Thêm sách vào giỏ hàng
    """
    book = get_object_or_404(Book, id=book_id)
    if book.stock <= 0:
        messages.error(request, "Cuốn sách này tạm thời đã có bạn đặt trước!")
        return redirect('store:book_detail', slug=book.slug)

    cart = request.session.get('cart', {})
    str_id = str(book_id)

    # Do sách cũ thường chỉ có 1 cuốn, giới hạn tối đa theo stock
    current_qty = cart.get(str_id, {}).get('quantity', 0)
    if current_qty < book.stock:
        cart[str_id] = {
            'quantity': current_qty + 1,
            'price': float(book.price)
        }
        messages.success(request, f"Đã thêm «{book.title}» vào giỏ hàng thành công!")
    else:
        messages.warning(request, f"Cuốn này tại Dino Books chỉ còn {book.stock} cuốn duy nhất!")

    request.session['cart'] = cart
    request.session.modified = True

    # Redirect hoặc quay lại trang trước
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'store:cart'
    return redirect(next_url)


def update_cart(request, book_id):
    """
    Cập nhật số lượng trong giỏ hàng
    """
    if request.method == 'POST':
        action = request.POST.get('action') # 'increase', 'decrease', or 'set'
        cart = request.session.get('cart', {})
        str_id = str(book_id)

        if str_id in cart:
            book = get_object_or_404(Book, id=book_id)
            current_qty = cart[str_id]['quantity']

            if action == 'increase':
                if current_qty < book.stock:
                    cart[str_id]['quantity'] += 1
                else:
                    messages.warning(request, f"Cuốn này chỉ còn {book.stock} cuốn trong kho!")
            elif action == 'decrease':
                if current_qty > 1:
                    cart[str_id]['quantity'] -= 1
                else:
                    del cart[str_id]
            elif action == 'remove':
                del cart[str_id]

            request.session['cart'] = cart
            request.session.modified = True

    return redirect('store:cart')


def remove_from_cart(request, book_id):
    """
    Xóa khỏi giỏ hàng
    """
    cart = request.session.get('cart', {})
    str_id = str(book_id)
    if str_id in cart:
        del cart[str_id]
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, "Đã bỏ sách khỏi giỏ hàng.")
    return redirect('store:cart')


# ==================== ĐẶT HÀNG & THANH TOÁN ====================

def checkout_view(request):
    """
    Trang thanh toán & nhập thông tin nhận sách
    """
    cart = request.session.get('cart', {})
    if not cart:
        messages.info(request, "Giỏ hàng của bạn đang trống. Hãy chọn thêm sách yêu thích nhé!")
        return redirect('store:book_list')

    cart_items = []
    subtotal = 0
    for book_id, item in cart.items():
        try:
            book = Book.objects.get(id=book_id)
            qty = item.get('quantity', 1)
            line_total = book.price * qty
            subtotal += line_total
            cart_items.append({
                'book': book,
                'quantity': qty,
                'line_total': line_total,
            })
        except Book.DoesNotExist:
            continue

    shipping_fee = 0 if subtotal >= 250000 else 25000
    total_amount = subtotal + shipping_fee

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        customer_email = request.POST.get('customer_email', '').strip()
        shipping_address = request.POST.get('shipping_address', '').strip()
        city = request.POST.get('city', '').strip()
        note = request.POST.get('note', '').strip()
        payment_method = request.POST.get('payment_method', 'cod')

        if not customer_name or not customer_phone or not shipping_address:
            messages.error(request, "Vui lòng điền đầy đủ Họ tên, Số điện thoại và Địa chỉ nhận hàng.")
            return render(request, 'store/checkout.html', {
                'cart_items': cart_items,
                'subtotal': subtotal,
                'shipping_fee': shipping_fee,
                'total_amount': total_amount,
            })

        # Tạo đơn hàng
        order = Order.objects.create(
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_email=customer_email,
            shipping_address=shipping_address,
            city=city,
            note=note,
            payment_method=payment_method,
            subtotal=subtotal,
            shipping_fee=shipping_fee,
            total_amount=total_amount,
            payment_status='paid' if payment_method == 'test' else 'unpaid',
            status='pending',
        )

        # Tạo OrderItem & giảm tồn kho
        for item in cart_items:
            book = item['book']
            OrderItem.objects.create(
                order=order,
                book=book,
                book_title=book.title,
                price=book.price,
                quantity=item['quantity']
            )
            # Trừ stock
            if book.stock >= item['quantity']:
                book.stock -= item['quantity']
                book.save()

        # Gửi email thông báo đơn hàng mới cho chủ tiệm
        send_order_notification_email(order)

        # Xóa giỏ hàng sau khi đặt thành công
        request.session['cart'] = {}
        request.session.modified = True

        return redirect('store:order_success', order_code=order.order_code)


    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_fee': shipping_fee,
        'total_amount': total_amount,
    }
    return render(request, 'store/checkout.html', context)


def order_success_view(request, order_code):
    """
    Trang thông báo đặt hàng thành công (Thanh toán khi nhận sách - COD)
    """
    order = get_object_or_404(Order, order_code=order_code)
    return render(request, 'store/order_success.html', {'order': order})


def order_tracking_view(request):
    """
    Tra cứu trạng thái đơn hàng qua Mã đơn hoặc Số điện thoại
    """
    orders = None
    query = request.GET.get('query', '').strip()
    
    if query:
        orders = Order.objects.filter(
            Q(order_code__iexact=query) | Q(customer_phone=query)
        ).order_by('-created_at')

    context = {
        'orders': orders,
        'query': query,
    }
    return render(request, 'store/order_tracking.html', context)


# ==================== KÝ GỬI & THANH LÝ SÁCH CŨ ====================

def trade_in_view(request):
    """
    Trang tiếp nhận sách thanh lý / ký gửi từ phụ huynh
    """
    if request.method == 'POST':
        contact_name = request.POST.get('contact_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        book_count = request.POST.get('book_count', 5)
        description = request.POST.get('description', '').strip()
        address = request.POST.get('address', '').strip()
        photo = request.FILES.get('photo')

        if not contact_name or not phone or not description:
            messages.error(request, "Vui lòng điền đủ Tên, Số điện thoại và danh sách sách muốn ký gửi.")
        else:
            TradeInRequest.objects.create(
                contact_name=contact_name,
                phone=phone,
                book_count=int(book_count) if str(book_count).isdigit() else 5,
                description=description,
                address=address,
                photo=photo
            )
            messages.success(request, "Cảm ơn ba/mẹ! Dino Books đã nhận được thông tin và sẽ liên hệ qua Zalo/SĐT trong vòng 24h để báo giá thu mua ạ!")
            return redirect('store:trade_in')

    return render(request, 'store/trade_in.html')


def about_view(request):
    """
    Giới thiệu Dino Books & Tiêu chuẩn tuyển chọn sách cũ
    """
    conditions = BookCondition.objects.all().order_by('-rating_percentage')
    return render(request, 'store/about.html', {'conditions': conditions})


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/admin/login/')
def shop_orders_dashboard(request):
    """
    Trang Quản trị Đơn hàng trực quan dành riêng cho chủ tiệm Dino Books
    Yêu cầu tài khoản admin mới xem được
    """
    status_filter = request.GET.get('status', '')
    orders = Order.objects.all().order_by('-created_at')
    
    if status_filter:
        orders = orders.filter(status=status_filter)

    # Thống kê nhanh
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    total_revenue = sum(o.total_amount for o in Order.objects.exclude(status='cancelled'))

    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')
        new_payment = request.POST.get('payment_status')
        tracking_num = request.POST.get('tracking_number')

        if order_id:
            order_obj = get_object_or_404(Order, id=order_id)

            # Xử lý nút từ chối đơn hàng (sự kiện bất khả kháng)
            if action == 'reject_order':
                if order_obj.status != 'cancelled':
                    # Hoàn trả lại số lượng sách vào kho
                    for item in order_obj.items.all():
                        if item.book:
                            item.book.stock += item.quantity
                            item.book.save()
                    order_obj.status = 'cancelled'
                    order_obj.save()
                    messages.warning(request, f"Đã từ chối đơn hàng #{order_obj.order_code}. Toàn bộ sách trong đơn đã được tự động hoàn lại vào kho!")
                return redirect('store:orders_dashboard')

            if new_status:
                order_obj.status = new_status
            if new_payment:
                order_obj.payment_status = new_payment
            if tracking_num is not None:
                order_obj.tracking_number = tracking_num.strip()
            order_obj.save()
            messages.success(request, f"Đã cập nhật đơn hàng #{order_obj.order_code} thành công!")
            return redirect('store:orders_dashboard')

    context = {
        'orders': orders,
        'status_filter': status_filter,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'total_revenue': total_revenue,
    }
    return render(request, 'store/orders_dashboard.html', context)


def manifest_view(request):
    """
    Khai báo Web App Manifest (PWA) cho thiết bị di động
    """
    manifest_data = {
        "name": "Dino Books",
        "short_name": "Dino Books",
        "description": "Website Bán Sách Tiếng Anh Cũ Tuyển Chọn Cho Thiếu Nhi & Trẻ Vị Thành Niên",
        "start_url": "/",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#ffffff",
        "theme_color": "#16a34a",
        "icons": [
            {
                "src": "/static/images/logo.png",
                "sizes": "192x192 512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ]
    }
    return JsonResponse(manifest_data)


def service_worker_view(request):
    """
    Service Worker phục vụ PWA cài đặt ứng dụng trên Android
    """
    js = """
self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', (event) => {
    event.respondWith(fetch(event.request));
});
"""
    return HttpResponse(js.strip(), content_type='application/javascript')


