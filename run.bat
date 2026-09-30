@echo off
chcp 65001 > nul
title Dino Books - Khởi Động Website
echo ========================================================
echo             DINO BOOKS - WEBSITE BÁN SÁCH CŨ
echo ========================================================
echo.
echo Đang khởi động hệ thống máy chủ Dino Books...
echo.

set PYTHON_CMD="C:\Users\tthau\AppData\Local\Programs\Python312\python.exe"
if not exist %PYTHON_CMD% (
    set PYTHON_CMD=python
)

start "" http://127.0.0.1:8088
echo Mở trình duyệt tại: http://127.0.0.1:8088
echo Đăng nhập Quản trị viên tại: http://127.0.0.1:8088/admin/
echo Tài khoản: admin / Mật khẩu: admindino123
echo.
echo Nhấn Ctrl + C để dừng máy chủ.
echo ========================================================
%PYTHON_CMD% manage.py runserver 0.0.0.0:8088
pause
