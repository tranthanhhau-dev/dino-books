import os
import datetime
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send_order_notification_email(order):
    """
    Gửi email thông báo đơn hàng mới cho chủ shop tại pttan.nv@gmail.com
    """
    to_email = getattr(settings, 'SHOP_NOTIFICATION_EMAIL', 'pttan.nv@gmail.com')
    subject = f"[Tiệm Sách Dino] 🔔 Đơn hàng mới #{order.order_code} từ {order.customer_name} ({int(order.total_amount):,}đ)"
    
    context = {'order': order}
    try:
        html_content = render_to_string('emails/order_notification.html', context)
        text_content = strip_tags(html_content)
    except Exception as e:
        print(f"Error rendering email template: {e}")
        text_content = f"Đơn hàng mới #{order.order_code} từ {order.customer_name}, SĐT: {order.customer_phone}, Tổng tiền: {order.total_amount:,.0f}đ"
        html_content = f"<p>{text_content}</p>"

    # Luôn ghi một bản sao vào thư mục media/email_logs để kiểm tra
    try:
        log_dir = os.path.join(settings.BASE_DIR, 'media', 'email_logs')
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"order_{order.order_code}_{datetime.date.today().strftime('%Y%m%d')}.html")
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    except Exception as e:
        print(f"Error saving email log copy: {e}")

    # Gửi qua hệ thống Email Django
    try:
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'Tiệm Sách Dino <pttan.nv@gmail.com>')
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=True)
        print(f"-> Email notification dispatched to {to_email} for order {order.order_code}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
