from .models import Category, AgeGroup, BookCondition

def store_context(request):
    """
    Cung cấp thông tin danh mục, độ tuổi, giỏ hàng vào mọi view
    """
    categories = Category.objects.all().order_by('order', 'name')
    age_groups = AgeGroup.objects.all().order_by('order', 'id')
    conditions = BookCondition.objects.all().order_by('-rating_percentage')
    
    # Tính giỏ hàng từ session
    cart = request.session.get('cart', {})
    cart_count = sum(item.get('quantity', 1) for item in cart.values())
    
    return {
        'all_categories': categories,
        'all_age_groups': age_groups,
        'all_conditions': conditions,
        'cart_count': cart_count,
        'shop_name': 'Tiệm Sách Dino',
        'shop_hotline': '0965.112.006',
        'shop_zalo': '0965112006',
        'shop_email': 'pttan.nv@gmail.com',
        'shop_address': 'Hà Nội & Giao hàng toàn quốc',
        'bank_info': {
            'bank_id': 'MB', # MBBank
            'account_no': '0965112006',
            'account_name': 'TIEM SACH DINO',
        }
    }
