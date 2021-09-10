cd /d %~dp0
%1 start "" mshta vbscript:createobject("shell.application").shellexecute("""%~0""","::",,"runas",1)(window.close)&exit
netsh interface ip set address name="WLAN" source=static addr=192.168.0.100 mask=255.255.255.0 