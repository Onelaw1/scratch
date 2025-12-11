@echo off
echo ==========================================
echo   네트워크 연결 복구 및 최적화 도구
echo ==========================================
echo.
echo 1. 관리자 권한 확인 중...
net session >nul 2>&1
if %errorLevel% == 0 (
    echo    관리자 권한: 확인됨
) else (
    echo    관리자 권한이 필요합니다. 우클릭 후 '관리자 권한으로 실행' 해주세요.
    pause
    exit
)

echo.
echo 2. IPv6 비활성화 (충돌 방지)...
powershell -Command "Disable-NetAdapterBinding -Name 'Wi-Fi' -ComponentID ms_tcpip6"

echo.
echo 3. DNS 서버를 Google DNS(8.8.8.8)로 고정...
netsh interface ipv4 set dnsservers "Wi-Fi" static 8.8.8.8 primary
netsh interface ipv4 add dnsservers "Wi-Fi" 8.8.4.4 index=2

echo.
echo 4. 네트워크 설정 초기화 (Winsock/IP)...
netsh winsock reset
netsh int ip reset

echo.
echo 5. DNS 캐시 삭제...
ipconfig /flushdns

echo.
echo ==========================================
echo   작업 완료! 
echo   인터넷 브라우저를 모두 닫았다가 다시 열어주세요.
echo ==========================================
pause
