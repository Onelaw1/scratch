@echo off
echo 네트워크 설정 복구 중 (IPv6 비활성화 + Google DNS)...
echo.

REM IPv6 비활성화 (Wi-Fi)
powershell -Command "Disable-NetAdapterBinding -Name 'Wi-Fi' -ComponentID ms_tcpip6"

REM IPv4 DNS 설정 (Google DNS)
netsh interface ipv4 set dnsservers "Wi-Fi" static 8.8.8.8 primary
netsh interface ipv4 add dnsservers "Wi-Fi" 8.8.4.4 index=2

REM DNS 캐시 초기화
ipconfig /flushdns

echo.
echo 설정이 완료되었습니다. 이제 네이버/빙 접속을 확인해보세요.
pause
