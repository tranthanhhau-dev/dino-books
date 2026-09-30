@echo off
chcp 65001 > nul
title Đẩy Mã Nguồn Dino Books Lên GitHub (tranthanhhau-dev/dino-books)
echo =========================================================================
echo             ĐẨY MÃ NGUỒN DINO BOOKS LÊN GITHUB
echo =========================================================================
echo.
echo Repository đích: https://github.com/tranthanhhau-dev/dino-books.git
echo.
echo LƯU Ý KHI GITHUB HỎI ĐĂNG NHẬP:
echo - Username: tranthanhhau-dev
echo - Password: Dán mã Personal Access Token (ghp_...)
echo   (Nếu chưa có Token, hãy mở https://github.com/settings/tokens/new,
echo    tích chọn 'repo' rồi bấm Generate token để lấy mã nhé)
echo =========================================================================
echo.
pause

echo Đang cấu hình remote và đẩy toàn bộ mã nguồn lên GitHub...
git_bin\cmd\git.exe remote remove origin 2>nul
git_bin\cmd\git.exe remote add origin https://github.com/tranthanhhau-dev/dino-books.git
git_bin\cmd\git.exe branch -M main
git_bin\cmd\git.exe push -u origin main

echo.
if %ERRORLEVEL% equ 0 (
    echo =========================================================================
    echo [THÀNH CÔNG] ĐÃ ĐẨY MÃ NGUỒN LÊN GITHUB HOÀN TẤT!
    echo Bây giờ bạn hãy mở https://dashboard.render.com để Deploy nhé!
    echo =========================================================================
) else (
    echo =========================================================================
    echo [LƯU Ý] Nếu đẩy thất bại do mật khẩu, bạn chỉ cần tạo Personal Access Token
    echo tại https://github.com/settings/tokens/new (chọn quyền repo) rồi dán vào nhé!
    echo =========================================================================
)
pause
