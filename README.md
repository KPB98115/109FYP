# 在開始Docker 之前需確保已安裝所需套件及軟體
## 系統環境要求
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Windows Terminal](https://apps.microsoft.com/store/detail/windows-terminal/9N0DX20HK701?hl=zh-tw&gl=tw&icid=CatNavSoftwareWindowsApps) (Optional)
- [Windows Subsystem for Linux(WSL 2)](https://learn.microsoft.com/zh-tw/windows/wsl/install)
# 透過遠端桌面連線／TeamViewer 遠端控制實驗室電腦
1.(TeamViewer)聯絡組長取得ID 及密碼，(遠端桌面連線)輸入IP 並登入實驗室電腦。  
2.開啟Docker Desktop  
3.開啟Windows Terminal：  
```
wsl -d Ubuntu
```  
4.查看Ubuntu distribution 是否在運行：  
```
wsl -l -v
```
5.在Windows Terminal 打開Ubuntu terminal，或是輸入以下指令進入Ubuntu terminal：  
```
wsl ~ -d Ubuntu
```
6.切換至Windows Terminal，在Docker Desktop 啟動Docker container：  
```
docker run -p 5000:5000 --gpus all [image_tag]
```
7.透過電腦的實體IP 位址連線進API server：
