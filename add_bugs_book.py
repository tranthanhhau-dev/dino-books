import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiem_sach_bot.settings')
django.setup()

from store.models import Book, Category, AgeGroup, BookCondition

age_group = AgeGroup.objects.get(slug='4-6-tuoi')
category = Category.objects.get(slug='board-lift-the-flap')
condition = BookCondition.objects.filter(rating_percentage__gte=95).order_by('-rating_percentage').first()
if not condition:
    condition = BookCondition.objects.first()

title = "BUGS: A Stunning Pop-Up Look at Insects, Spiders, and Other Creepy-Crawlies"

book, created = Book.objects.get_or_create(
    title=title,
    defaults={
        'vietnamese_title': 'Sách Pop-Up Dựng Hình 3D Khổng Lồ: Thế Giới Côn Trùng & Bọ Cánh Cứng',
        'author': 'George McGavin (Minh họa: Jim Kay)',
        'publisher': 'Candlewick Press / Walker Books',
        'category': category,
        'age_group': age_group,
        'condition': condition,
        'condition_detail': 'Sách Pop-up 3D tuyệt đẹp, cơ chế dựng hình nổi 3D hoạt động hoàn hảo 100%, không rách, không gãy gập khớp chuyển động, bìa cứng cáp bóng đẹp.',
        'original_price': 520000,
        'price': 485000,
        'stock': 1,
        'reading_level': 'Ages 4-8 / 3D Pop-Up Science',
        'pages': 16,
        'cover_type': 'flap_sound',
        'publication_year': 2013,
        'isbn': '978-0763667627',
        'description': """Một siêu phẩm sách Pop-up 3D kỳ ảo về thế giới côn trùng dành cho các nhà thám hiểm nhí! Được viết bởi tiến sĩ George McGavin (nhà côn trùng học Đại học Oxford) và minh họa bởi Jim Kay (họa sĩ lừng danh minh họa Harry Potter bản màu).

Điểm nổi bật của cuốn sách:
• Các mô hình Pop-up 3D khổng lồ bật tung sống động khi mở trang: mô hình bọ khổng lồ với các cánh lật mở cấu tạo bên trong, tổ ong vò vẽ 3D với ấu trùng và ong chúa, nhện tarantula chân xanh...
• Hàng chục cánh lật nhỏ (flaps) giải mã bí mật sinh học: cách côn trùng thở, cơ chế nhìn của mắt kép, hệ thần kinh và cách săn mồi.
• Tranh vẽ tay kỳ công, màu sắc chân thực vừa khoa học vừa đầy tính nghệ thuật.

Món quà tuyệt vời kích thích niềm say mê khám phá khoa học tự nhiên và rèn luyện kỹ năng đọc tiếng Anh cho bé!""",
        'cover_image': 'books/covers/bugs_popup_cover.jpg',
        'extra_image_1': 'books/extras/bugs_popup_cockroach_full.jpg',
        'extra_image_2': 'books/extras/bugs_popup_cockroach_detail.jpg',
        'extra_image_3': 'books/extras/bugs_popup_wasp_nest.jpg',
        'is_featured': True,
        'is_hot_deal': False,
    }
)

if not created:
    book.vietnamese_title = 'Sách Pop-Up Dựng Hình 3D Khổng Lồ: Thế Giới Côn Trùng & Bọ Cánh Cứng'
    book.age_group = age_group
    book.category = category
    book.original_price = 520000
    book.price = 485000
    book.cover_image = 'books/covers/bugs_popup_cover.jpg'
    book.extra_image_1 = 'books/extras/bugs_popup_cockroach_full.jpg'
    book.extra_image_2 = 'books/extras/bugs_popup_cockroach_detail.jpg'
    book.extra_image_3 = 'books/extras/bugs_popup_wasp_nest.jpg'
    book.is_featured = True
    book.save()

print(f"SUCCESS: Book registered with ID={book.id}, slug={book.slug}, price={book.price}, age={book.age_group.name}")
