@echo off
echo Wi-Fi 최적 속도 재연결 스크립트
echo ================================
echo.
echo Wi-Fi 연결 해제 중...
netsh wlan disconnect
timeout /t 3 /nobreak >nul
echo.
echo Wi-Fi 재연결 중...
netsh wlan connect name="Strategy_5G"
timeout /t 5 /nobreak >nul
echo.
echo 현재 연결 상태:
netsh wlan show interfaces | findstr "수신 전송 신호"
echo.
echo 완료! 속도 테스트를 해보세요.
pause
