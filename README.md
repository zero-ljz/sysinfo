# 跨平台系统探针

通过 WebSocket 实时展示服务器的 CPU、内存、磁盘、网络、进程和 TCP 连接等系统信息。一个页面可同时监控多台服务器，并会在连接中断后自动重连。

## 环境要求

- Python 3
- `pip`

## 安装

```bash
git clone https://github.com/zero-ljz/sysinfo.git
cd sysinfo

python3 -m venv .venv
.venv/bin/python3 -m pip install --upgrade pip
.venv/bin/python3 -m pip install -r requirements.txt
```

## 启动服务

```bash
.venv/bin/python3 app.py --host 0.0.0.0 --port 8000
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--host` / `-H` | `0.0.0.0` | 服务监听地址 |
| `--port` / `-p` | `8000` | 服务监听端口 |

需要在后台运行时：

```bash
nohup .venv/bin/python3 app.py --host 0.0.0.0 --port 8000 > sysinfo.log 2>&1 &
```

## 访问监控页面

服务启动后，在浏览器打开：

```text
http://<server-host>:8000/
```

对应的 WebSocket 地址为：

```text
ws://<server-host>:8000/ws/
```

`index.html` 也可以直接用浏览器打开。要在同一页面监控多台服务器，请通过 `urls` 查询参数传入以逗号分隔的 WebSocket 地址：

```text
http://127.0.0.1:8000/?urls=ws://host1:8000/ws/,ws://host2:8000/ws/
```

## 停止后台服务

```bash
pkill -f 'app.py.*--port 8000'
```

## 平台安装说明

在 Debian 或 Ubuntu 上，也可使用系统包安装依赖：

```bash
sudo apt install python3-bottle python3-gevent-websocket python3-py-cpuinfo python3-psutil
```

在 Alpine 上：

```bash
pip3 install bottle==0.12.25 gevent-websocket py-cpuinfo==9.0.0
apk add py3-psutil
```
