# 跨平台系统探针

**克隆代码**  
git clone https://github.com/zero-ljz/sysinfo.git
cd sysinfo

**安装依赖**  
pip install -r requirements.txt

**启动服务器**
python3 app.py

**使用说明**  
* index.html文件支持直接在本地用浏览器打开  
* 支持在一个页面查看多台服务器
* 访问静态文件时可以从url的参数中传入多个服务器的url  
http://127.0.0.1:3000/?urls=ws://your_host1:3000/ws/,ws://your_host2:3000/ws/