@echo off
REM Wi-Fi 자동 재연결 스크립트 (로그인 시 자동 실행)
REM 30초 대기 후 Wi-Fi 재연결하여 최적 속도 확보

REM 네트워크 안정화를 위해 30초 대기
timeout /t 30 /nobreak >nul

REM Wi-Fi 연결 해제
netsh wlan disconnect >nul 2>&1

REM 3초 대기
timeout /t 3 /nobreak >nul

REM Wi-Fi 재연결
netsh wlan connect name="Strategy_5G" >nul 2>&1

REM 로그 기록 (선택사항)
echo %date% %time% - Wi-Fi 자동 재연결 완료 >> "%USERPROFILE%\wifi_reconnect.log"

exit
