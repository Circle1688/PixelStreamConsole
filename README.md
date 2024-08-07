# 像素流送

## 云服务器准备

申请一个云服务器，有公网IP，系统在windows server 2019以上

### OpenSSH

在系统设置里安装OpenSSH客户端和服务端

### 安全组

云服务器安全组打开所有端口

### 关闭账户锁定

右键单击开始，然后单击运行(R)。在运行对话框中输入`gpedit.msc`命令，然后单击确定，进入本地组策略编辑器页面

在本地组策略编辑器页面中，选择计算机配置 > Windows设置 > 安全设置 > 账户策略 > 账户锁定策略

在账户锁定策略页面，双击账户锁定阈值，进入账户锁定阈值 属性窗口

在账户锁定阈值 属性窗口，将阈值修改为0，单击确定



## 部署 - STUN/TURN服务器

使用coturn（内网穿透）实现云服务器运行matchmaker、信令服务器，本地高性能电脑（家庭网络）运行ue实例，通过公网访问



### 移除nodejs环境检查

编辑`Start_Common.ps1`

注释掉 有关setup.bat的脚本

```powershell
Start-Process -FilePath "$PSScriptRoot\setup.bat"
```

 即可绕开环境检查 nodejs，加快启动速度，但是第一次部署必须手动去运行setup.bat去安装环境

### 移除公网IP检测

注释掉 

```powershell
$global:PublicIP = Invoke-WebRequest -Uri "https://api.ipify.org" -UseBasicParsing
```

 这个是用来通过一个网页来获取公网ip的 我们直接通过参数指定

### 修改TURN的LocalIp

编辑`Start_TURNServer.ps1`

注释掉

```powershell
$LocalIP = (Test-Connection -ComputerName (hostname) -Count 1  | Select IPV4Address).IPV4Address.IPAddressToString
```

写上

```powershell
$LocalIP = "127.0.0.1"
```



### 分开启动TURN和信令服务器

编辑`Start_WithTURN_SignallingServer.ps1`

注释掉 

```
Start-Process -FilePath "PowerShell" -ArgumentList ".\Start_TURNServer.ps1" -WorkingDirectory "$PSScriptRoot"
```

### 创建批处理脚本

创建bat脚本 run_start_turn.bat

```bat
start powershell .\Start_TURNServer.ps1 --publicip <服务器的公网ip地址>
```



创建bat脚本 run_SignallingServer.bat

```bat
start powershell .\Start_WithTURN_SignallingServer.ps1 --publicip <服务器的公网ip地址> --HttpPort <例如91> --StreamerPort <例如9988> --SFUPort <例如9989> --UseMatchmaker true --HomepageFile <例如player_file.html>
```



### UE启动命令参数

```bat
-AudioMixer -PixelStreamingIP=<服务器的公网ip地址> -PixelStreamingPort=<例如9988> -RenderOffScreen -ForceRes -ResX=<例如1920> -ResY=<例如1080>
```



### 启动顺序

例如启动一个多人的服务

1. 启动matchmaker `Matchmaker\platform_scripts\cmd\run.bat` 要注释掉跟setup.bat有关的脚本，绕开nodejs检查

2. 启动一个turn服务器 `run_start_turn.bat`

3. 启动多个信令服务器 `run_SignallingServer.bat`

4. 启动多个对应的ue实例