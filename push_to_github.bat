@echo off
chcp 65001 > nul
title Đẩy Mã Nguồn Dino Books Lên GitHub
echo =========================================================================
echo             ĐẨY MÃ NGUỒN DINO BOOKS LÊN GITHUB
echo =========================================================================
echo.
echo Bước 1: Hãy đăng nhập https://github.com và tạo 1 repository mới:
echo         - Đặt tên Repository: dino-books (hoặc tùy chọn)
echo         - Để chế độ Public hoặc Private
echo         - Không tích chọn "Add a README file"
echo.
echo Bước 2: Dán đường link Repository của bạn vào bên dưới (đuôi .git)
echo         Ví dụ: https://github.com/ten-cua-ban/dino-books.git
echo.
set /p REPO_URL="Nhập link GitHub Repository: "

if "%REPO_URL%"=="" (
    echo Bạn chưa nhập link. Hãy chạy lại file nhé.
    pause
    exit /b
)

echo.
echo Đang cấu hình và đẩy mã nguồn lên GitHub...
git_bin\cmd\git.exe remote remove origin 2>nul
git_bin\cmd\git.exe remote add origin %REPO_URL%
git_bin\cmd\git.exe branch -M main
git_bin\cmd\git.exe push -u origin main

echo.
echo =========================================================================
echo ĐÃ HOÀN TẤT ĐẨY MÃ NGUỒN LÊN GITHUB!
echo Bây giờ bạn hãy mở https://dashboard.render.com và làm theo hướng dẫn.
echo =========================================================================
pause
