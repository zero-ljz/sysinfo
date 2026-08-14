# Sysinfo

一个基于 Python、psutil 和 WebSocket 的轻量级跨平台系统监控面板。它会每秒采集并推送服务器状态，可在同一页面实时查看一台或多台主机，并在连接中断后自动重连。

## 功能

- 查看操作系统、主机名、CPU 型号、架构、内网 IP 和系统运行时间
- 监控 CPU 使用率、频率、核心数、线程数与系统负载
- 监控内存和交换空间的容量与使用率
- 监控根分区容量、磁盘累计读写量与实时读写速度
- 监控网络累计收发量与实时传输速度
- 查看进程数量以及 IPv4、IPv6 TCP 连接数
- 通过一个页面同时监控多台服务器
- WebSocket 断开后每 3 秒自动尝试重连

## 运行要求

- Python 3
- pip

## 快速开始

克隆仓库并创建虚拟环境：

```bash
git clone https://github.com/zero-ljz/sysinfo.git
cd sysinfo
python -m venv .venv
```

Linux 或 macOS：

```bash
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

Windows PowerShell：

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe app.py
```

服务默认监听 `0.0.0.0:8000`。启动后打开：

```text
http://127.0.0.1:8000/
```

页面默认连接当前服务的 WebSocket 地址：

```text
ws://127.0.0.1:8000/ws/
```

## 多主机监控

先在每台待监控主机上启动本项目，然后通过页面的 `urls` 查询参数传入多个 WebSocket 地址，地址之间使用英文逗号分隔：

```text
http://127.0.0.1:8000/?urls=ws://host1:8000/ws/,ws://host2:8000/ws/
```

`index.html` 也可以直接在浏览器中打开。此时需要使用 `urls` 参数明确指定至少一个 WebSocket 地址。

## 启动参数

```text
usage: app.py [-h] [--host HOST] [--port PORT]
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--host` / `-H` | `0.0.0.0` | 服务监听地址 |
| `--port` / `-p` | `8000` | 服务监听端口 |

例如，仅允许本机访问并监听 `9000` 端口：

```bash
.venv/bin/python app.py --host 127.0.0.1 --port 9000
```

## 后台运行

在 Linux 上可以使用 `nohup`：

```bash
nohup .venv/bin/python app.py --host 0.0.0.0 --port 8000 > sysinfo.log 2>&1 &
```

停止该后台进程：

```bash
pkill -f 'app.py.*--port 8000'
```

长期运行时，建议使用 systemd、Supervisor 或其他进程管理工具托管服务。

## 项目结构

| 文件 | 说明 |
| --- | --- |
| `app.py` | 采集系统信息，并通过 WebSocket 每秒推送一次数据 |
| `index.html` | 展示监控数据、计算实时传输速度并处理自动重连 |
| `requirements.txt` | Python 依赖列表 |

## 安全说明

本项目当前未提供身份认证和访问控制，并会暴露主机及资源使用信息。请勿直接将服务端口开放到公网；建议将其部署在可信网络中，或通过带有 HTTPS、WSS 和身份认证的反向代理提供访问。

在部分操作系统上，获取系统级 TCP 连接信息可能需要更高权限。
