import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiem_sach_bot.settings')
django.setup()

from store.models import Book, Category, AgeGroup, BookCondition

age_group = AgeGroup.objects.get(slug='4-6-tuoi')
cat_pic = Category.objects.get(slug='picture-books')
cat_stem = Category.objects.get(slug='science-stem')
cat_phonics = Category.objects.get(slug='phonics')

condition = BookCondition.objects.filter(rating_percentage=85).first()
if not condition:
    condition = BookCondition.objects.filter(rating_percentage__lte=90).first()

batch2_books = [
    {
        "title": "Ten-Minute Stories: The Brave Tin Soldier and Other Stories",
        "vietnamese_title": "Chú Lính Chì Dũng Cảm & Tuyển Tập Truyện 10 Phút Trước Giờ Ngủ",
        "author": "Hans Christian Andersen (Miles Kelly Retold)",
        "publisher": "Miles Kelly Publishing UK",
        "category": cat_pic,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Bìa màu tươi tắn, ruột sách sạch đẹp, tập hợp các truyện cổ tích kinh điển 10 phút ngắn gọn.",
        "original_price": 160000,
        "price": 35000,
        "stock": 5,
        "reading_level": "Bedtime Tales / Ages 4-8",
        "pages": 40,
        "cover_type": "paperback",
        "publication_year": 2018,
        "isbn": "978-1786178343",
        "cover_image": "books/covers/the_brave_tin_soldier.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Tuyển tập truyện đọc ngắn 10 phút trước giờ đi ngủ kinh điển của nhà xuất bản Miles Kelly (Anh Quốc).
• Chú Lính Chì Dũng Cảm trên chiếc thuyền giấy phiêu lưu qua cống ngầm và lòng cá, giữ vững tình yêu kiên định với cô vũ nữ ba-lê giấy.
• Minh họa màu nước bay bổng, giàu chất thơ và cảm xúc.
• Ngôn từ tiếng Anh trong sáng, độ dài mỗi truyện chỉ khoảng 10 phút, lý tưởng để bố mẹ đọc cho con trước khi ngủ."""
    },
    {
        "title": "Disney's Atlantis: The Lost Empire",
        "vietnamese_title": "Atlantis: Đế Chế Thất Lạc (Ấn bản Ladybird kinh điển)",
        "author": "Disney Storybook Artists",
        "publisher": "Ladybird Books UK",
        "category": cat_pic,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Ấn bản Ladybird con bọ rùa nổi tiếng, gáy chắc, màu in hoạt hình Disney sống động.",
        "original_price": 140000,
        "price": 35000,
        "stock": 5,
        "reading_level": "Ladybird Disney / Ages 4-8",
        "pages": 32,
        "cover_type": "paperback",
        "publication_year": 2017,
        "isbn": "",
        "cover_image": "books/covers/disney_atlantis_the_lost_empire.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Cuộc phiêu lưu thám hiểm đáy biển sâu đầy bí ẩn của hãng phim hoạt hình Walt Disney!
• Cùng nhà ngôn ngữ học trẻ Milo Thatch và đoàn tàu ngầm vượt qua quái vật Leviathan để khám phá thành phố cổ đại Atlantis rực rỡ dưới lòng đại dương.
• Câu từ tiếng Anh phiêu lưu súc tích, kèm hình ảnh trích từ phim sắc nét.
• Rất thích hợp cho các bé trai mê phiêu lưu, tàu ngầm và khám phá thế giới bí ẩn."""
    },
    {
        "title": "One Ted Falls Out of Bed",
        "vietnamese_title": "Chú Gấu Ted Ngã Khỏi Giường (Tác giả Julia Donaldson - Tác giả The Gruffalo)",
        "author": "Julia Donaldson (Minh họa: Anna Currey)",
        "publisher": "Macmillan Children's Books",
        "category": cat_pic,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Bìa vàng ấm áp, gáy chắc, ruột sạch sẽ, câu chuyện đếm số từ 1 đến 10 bằng tiếng Anh có vần điệu.",
        "original_price": 180000,
        "price": 35000,
        "stock": 5,
        "reading_level": "Counting & Rhyme / Ages 2-6",
        "pages": 32,
        "cover_type": "paperback",
        "publication_year": 2019,
        "isbn": "978-1509804863",
        "cover_image": "books/covers/one_ted_falls_out_of_bed.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Tác phẩm xuất sắc của nữ văn sĩ Julia Donaldson - tác giả của bộ truyện The Gruffalo lừng danh toàn cầu!
• Chú gấu bông Ted trượt chân ngã khỏi giường trong đêm và gặp gỡ các bạn đồ chơi: 2 chú chuột tí hon mang kèn đồng, 3 chú ếch tinh nghịch nhảy nhót, 4 chiếc ô tô đồ chơi...
• Vần điệu tiếng Anh ngân nga, vui nhộn giúp bé ghi nhớ số đếm từ 1 đến 10 một cách tự nhiên.
• Cuốn sách gối đầu giường ngọt ngào xoa dịu những giấc mơ của bé thơ."""
    },
    {
        "title": "Woody Woodpecker: Amazing Animal Disguises",
        "vietnamese_title": "Chim Gõ Kiến Woody: Tài Ngụy Trang Kỳ Thú Của Động Vật (STEM Khoa Học)",
        "author": "Universal Studios / Dalmatian Press",
        "publisher": "Dalmatian Press USA",
        "category": cat_stem,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Bìa bóng đẹp, ruột sạch sẽ, hình ảnh chụp thực tế thế giới động vật ngụy trang sắc nét.",
        "original_price": 150000,
        "price": 35000,
        "stock": 5,
        "reading_level": "Nature & Science / Ages 4-8",
        "pages": 24,
        "cover_type": "paperback",
        "publication_year": 2018,
        "isbn": "",
        "cover_image": "books/covers/woody_woodpecker_amazing_animal_disguises.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Cùng nhân vật hoạt hình chim gõ kiến Woody Woodpecker lém lỉnh khám phá siêu năng lực ngụy trang của động vật!
• Khám phá vì sao loài hổ lại có bộ lông vằn vện giữa đồng cỏ, loài bọ lá có thể ẩn mình hoàn hảo như chiếc lá thật, và tắc kè đổi màu trên thân cây.
• Tranh vẽ hoạt hình kết hợp ảnh chụp thật động vật tự nhiên sống động.
• Kích thích tình yêu thiên nhiên và bổ sung từ vựng khoa học sinh học tiếng Anh cho bé."""
    },
    {
        "title": "Collins Big Cat Phonics: Pod Digs a Pit",
        "vietnamese_title": "Collins Big Cat: Chú Cướp Biển Nhí Pod Đào Hố (Luyện Đánh Vần Phonics Band Pink B)",
        "author": "Clare Helen Welsh (Minh họa: Michael Emmerson)",
        "publisher": "HarperCollins Publishers UK",
        "category": cat_phonics,
        "age_group": age_group,
        "condition": condition,
        "condition_detail": "Ấn bản Collins Big Cat chuẩn quốc tế, giấy in bóng đẹp sạch sẽ, luyện đọc ngữ âm cho bé mầm non.",
        "original_price": 130000,
        "price": 35000,
        "stock": 5,
        "reading_level": "Phonics Band Pink B / Stage 1+",
        "pages": 16,
        "cover_type": "paperback",
        "publication_year": 2020,
        "isbn": "978-0008416485",
        "cover_image": "books/covers/collins_big_cat_pod_digs_a_pit.jpg",
        "is_featured": True,
        "is_hot_deal": True,
        "description": """Thuộc hệ thống sách đọc phân cấp hàng đầu vương quốc Anh Collins Big Cat Phonics của NXB HarperCollins!
• Chú cướp biển nhí Pod cùng chú vẹt cưng đi tìm kho báu trên bãi biển cát vàng.
• Được thiết kế chuyên biệt để luyện tập các âm phonics cơ bản: p, o, d, i, g, s, a, t.
• Tranh vẽ đáng yêu, câu từ ngắn giúp bé tự tin ghép vần và tự đọc được trọn vẹn cuốn sách tiếng Anh đầu tiên."""
    },
]

for b_data in batch2_books:
    title = b_data['title']
    book, created = Book.objects.get_or_create(title=title, defaults=b_data)
    if not created:
        for k, v in b_data.items():
            setattr(book, k, v)
        book.save()
    print(f"BATCH2_SAVED: id={book.id}, slug={book.slug}, price={book.price}, stock={book.stock}")

print("SUCCESS_BATCH2_ADDED")
