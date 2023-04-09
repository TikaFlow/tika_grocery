Set ws = CreateObject("WScript.Shell")
ws.CurrentDirectory = "D:\your\path"
rem 检测网络
ws.Run "nettest.bat", 0, true
rem 启动心跳
ws.Run "heartBeat.bat", 0
rem 订阅消息
ws.Run "cmd /k mqttx.exe sub --config >powerInfo.log", 0
rem 处理消息
ws.Run "monitor.bat", 0
