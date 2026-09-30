@echo off
chcp 65001 > nul
title Dino Books - Chạy Web App Online (HTTPS)
echo ========================================================
echo             DINO BOOKS - CHẠY WEB & CLOUDFLARE TUNNEL
echo ========================================================
echo.
echo 1. Đang khởi động Django Server (Cổng 8088)...
start "Django Server - Dino Books" cmd /c "python manage.py runserver 0.0.0.0:8088"

timeout /t 3 /nobreak > nul

echo.
echo 2. Đang kết nối Cloudflare Tunnel tạo link HTTPS an toàn...
echo.
echo =========================================================================
echo HƯỚNG DẪN:
echo Sao chép đường link "https://xxxx.trycloudflare.com" hiển thị bên dưới,
echo gửi vào Zalo/mở trên Chrome điện thoại Android -> Bấm "Cài đặt ứng dụng"!
echo =========================================================================
echo.
cloudflared.exe tunnel --url http://127.0.0.1:8088
pause
