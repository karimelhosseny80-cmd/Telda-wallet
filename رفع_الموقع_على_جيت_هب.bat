@echo off
chcp 65001 > nul
echo ========================================================
echo 🚀 جاري رفع محفظة تيلدا إلى حسابك على GitHub...
echo ========================================================
echo.
git add .
git commit -m "feat: latest portfolio update with holding durations and Gemini Pro"
echo.
echo جاري إرسال الملفات إلى مستودع Telda-wallet...
echo (إذا ظهرت لك نافذة في المتصفح، اضغط Sign in with your browser)
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo ✅ تم رفع الموقع بنجاح إلى GitHub!
    echo.
    echo رابط مستودعك:
    echo https://github.com/karimelhosseny80-cmd/Telda-wallet
    echo.
    echo رابط موقعك المباشر على GitHub Pages:
    echo https://karimelhosseny80-cmd.github.io/Telda-wallet/
    echo ========================================================
    start https://karimelhosseny80-cmd.github.io/Telda-wallet/
) else (
    echo.
    echo ⚠️ حدث خطأ أثناء الإرسال.
)
echo.
pause
