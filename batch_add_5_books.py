import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiem_sach_bot.settings')
django.setup()

from store.models import Book, Category, AgeGroup, BookCondition

# Get or match references
age_group = AgeGroup.objects.get(slug='4-6-tuoi')
cat_pic = Category.objects.get(slug='picture-books')
condition = BookCondition.objects.filter(rating_percentage=85).first()
if not condition:
    condition = BookCondition.objects.filter(rating_percentage__lte=90).first()

books_to_add = [
    {
        "title": "Out on bikes with Grampy",
        "vietnamese_title": "Đạp Xe Cùng Ông Ngoại (Câu chuyện gia đình ấm áp)",
        "author": "Anna Jarvis (Minh họa: Hannah Asen)",
        "publisher": "Play Together on Pedals",
        "category": cat_pic,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Bìa mềm, gáy chắc chắn, ruột sách sạch sẽ, tranh màu tươi tắn, không viết vẽ.",
        "original_price": 120000,
        "price": 30000,
        "stock": 1,
        "reading_level": "Early Picture Book / Ages 3-6",
        "pages": 24,
        "cover_type": "paperback",
        "publication_year": 2017,
        "isbn": "",
        "cover_image": "books/covers/out_on_bikes_with_grampy.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Một câu chuyện gia đình ngọt ngào về chuyến đạp xe dạo chơi ven hồ của hai ông cháu và chú cún đốm.
• Tranh minh họa màu nước trong trẻo, nét vẽ gần gũi.
• Giúp bé 3-6 tuổi làm quen từ vựng tiếng Anh về hoạt động ngoài trời, thiên nhiên và các con vật (chim mòng biển, vịt nước, cún con).
• Nuôi dưỡng tình cảm gắn bó yêu thương giữa ông bà và các cháu nhỏ."""
    },
    {
        "title": "101 Dalmatians (Disney)",
        "vietnamese_title": "101 Chú Chó Đốm (Truyện tranh kinh điển của Disney)",
        "author": "Disney Storybook Artists",
        "publisher": "Disney Press",
        "category": cat_pic,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Bìa vuông vắn viền khung xương chó đáng yêu, ruột sách sạch đẹp, màu in sắc nét chuẩn Disney.",
        "original_price": 140000,
        "price": 30000,
        "stock": 1,
        "reading_level": "Disney Classic / Ages 3-7",
        "pages": 32,
        "cover_type": "paperback",
        "publication_year": 2018,
        "isbn": "",
        "cover_image": "books/covers/101_dalmatians.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Tác phẩm kinh điển vượt thời gian được hàng triệu bạn nhỏ trên toàn thế giới mê đắm!
• Theo chân cặp vợ chồng chó Pongo và Perdita cùng nhau vượt qua muôn vàn gian nan để giải cứu đàn con đốm thoát khỏi bàn tay của mụ Cruella de Vil.
• Câu văn tiếng Anh ngắn gọn, súc tích, ngữ pháp căn bản dễ hiểu cho bé mầm non và tiểu học.
• Hình ảnh sinh động, biểu cảm ngộ nghĩnh của đàn chó con khiến bé thích thú đọc đi đọc lại nhiều lần."""
    },
    {
        "title": "Can't You Sleep, Little Bear?",
        "vietnamese_title": "Gấu Nhỏ Chưa Ngủ Được À? (Kiệt tác truyện ru ngủ đạt giải thưởng quốc tế)",
        "author": "Martin Waddell (Minh họa: Barbara Firth)",
        "publisher": "Walker Books UK",
        "category": cat_pic,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Ấn bản Walker Books chuẩn Anh, gáy thẳng đẹp, giấy ruột ngà ấm mắt, đạt giải thưởng Kate Greenaway Medal & The Smarties Prize.",
        "original_price": 180000,
        "price": 30000,
        "stock": 1,
        "reading_level": "Bedtime Classic / Lexile 510L",
        "pages": 32,
        "cover_type": "paperback",
        "publication_year": 2019,
        "isbn": "978-0744526011",
        "cover_image": "books/covers/cant_you_sleep_little_bear.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Kiệt tác truyện đọc trước giờ đi ngủ (Bedtime Story) danh giá bậc nhất thế giới!
• Chú Gấu Nhỏ sợ bóng tối trong hang sâu nên trằn trọc mãi không ngủ được. Bác Gấu Lớn kiên nhẫn thắp từng chiếc đèn lồng từ nhỏ đến lớn, rồi nhẹ nhàng bế gấu nhỏ ra cửa hang chỉ cho bé ngắm vầng trăng rực sáng dịu êm.
• Giọng văn ấm áp, vỗ về tâm lý sợ bóng tối của trẻ nhỏ, giúp bé chìm vào giấc ngủ an lành.
• Cuốn sách gối đầu giường được các chuyên gia giáo dục sớm khuyên đọc."""
    },
    {
        "title": "Supertato",
        "vietnamese_title": "Khoai Tây Siêu Nhân Supertato (Truyện tranh cười bán chạy số 1 nước Anh)",
        "author": "Sue Hendra & Paul Linnet",
        "publisher": "Simon & Schuster Children's Books",
        "category": cat_pic,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Bìa bóng ép nhũ chữ Supertato lấp lánh, ruột sách sạch sẽ, tranh màu rực rỡ vui nhộn.",
        "original_price": 190000,
        "price": 30000,
        "stock": 1,
        "reading_level": "Humor & Adventure / Lexile 480L",
        "pages": 32,
        "cover_type": "paperback",
        "publication_year": 2018,
        "isbn": "978-1471120978",
        "cover_image": "books/covers/supertato.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Series truyện tranh thiếu nhi siêu hài hước làm mưa làm gió tại Anh và các nước nói tiếng Anh!
• Ai bảo khoai tây chỉ để luộc? Chú củ khoai tây tròn xoe đeo mặt nạ đen, khoác áo choàng đỏ trở thành siêu anh hùng Supertato bảo vệ gian hàng siêu thị khỏi hạt đậu xanh tí hon xấu tính Evil Pea vừa trốn khỏi tủ đông!
• Cốt truyện hồi hộp, bất ngờ và tràn ngập tiếng cười giòn giã.
• Giúp bé thêm yêu thích các loại rau củ quả trong bữa ăn hàng ngày."""
    },
    {
        "title": "The Art Lesson",
        "vietnamese_title": "Tiết Học Vẽ Của Tommy (Truyện truyền cảm hứng sáng tạo nghệ thuật cho bé)",
        "author": "Tomie dePaola",
        "publisher": "Putnam / Sandcastle Books",
        "category": cat_pic,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Bìa viền vàng ấm áp, gáy chắc chắn, ruột sạch 100%, nét vẽ mực kinh điển của danh họa Tomie dePaola.",
        "original_price": 170000,
        "price": 30000,
        "stock": 1,
        "reading_level": "Ages 4-8 / Art & Creativity",
        "pages": 32,
        "cover_type": "paperback",
        "publication_year": 2017,
        "isbn": "978-0698115729",
        "cover_image": "books/covers/the_art_lesson.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Tác phẩm tự truyện kinh điển của họa sĩ Tomie dePaola tôn vinh trí tưởng tượng và cá tính sáng tạo của trẻ nhỏ!
• Cậu bé Tommy đam mê vẽ tranh từ thuở bé và luôn ước mơ trở thành họa sĩ. Nhưng khi vào lớp một, cô giáo dạy vẽ lại yêu cầu cả lớp phải tô màu theo mẫu giống hệt nhau...
• Câu chuyện giàu tính nhân văn, khuyến khích các bạn nhỏ dám theo đuổi đam mê và tự do thể hiện thế giới nội tâm qua nét cọ.
• Lựa chọn tuyệt vời cho các bé thích vẽ tranh, tô màu và làm quen tiếng Anh nghệ thuật."""
    },
]

for b_data in books_to_add:
    title = b_data['title']
    book, created = Book.objects.get_or_create(title=title, defaults=b_data)
    if not created:
        for k, v in b_data.items():
            setattr(book, k, v)
        book.save()
    print(f"SAVED: id={book.id}, slug={book.slug}, price={book.price}")

print("SUCCESS_ALL_5_BOOKS_ADDED")
