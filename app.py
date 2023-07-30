import datetime
import platform
import json
import socket
import time

import psutil
import cpuinfo
import gevent.monkey
from bottle import Bottle, request, abort, run, static_file
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

gevent.monkey.patch_all()

app = Bottle()

# WebSocket连接集合，用于存储所有已连接的客户端
connected_websockets = set()

# WebSocket处理类
class SystemProbeWebSocket:
    def __init__(self, ws):
        self.ws = ws

    def send_system_info(self):
        cpu_info = cpuinfo.get_cpu_info()
        while True:
            system_info = {
                "os": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": cpu_info['brand_raw'],
                "node": platform.node(),

                "cpu_usage": psutil.cpu_percent(),
                "cpu_freq": psutil.cpu_freq().current,
                "cpu_cores": psutil.cpu_count(logical=True),
                "memory": psutil.virtual_memory()._asdict(),
                "swap": psutil.swap_memory()._asdict(),
                "disk": psutil.disk_usage('/')._asdict(),
                "disk_io": psutil.disk_io_counters()._asdict(),
                "network": psutil.net_io_counters()._asdict(),
                "load_avg": psutil.getloadavg(),
                "process_count": len(psutil.pids()),
                "boot_time": int(psutil.boot_time()),
                #"ip_address": socket.gethostbyname(socket.gethostname()),
                "timestamp": int(time.time()),
                "current_time": str(datetime.datetime.now()),
                "time_zone": datetime.datetime.now().astimezone().tzinfo.tzname(None),
            }

            # 将系统信息转换为 JSON 字符串
            json_data = json.dumps(system_info)

            # 将 JSON 字符串发送给客户端
            self.ws.send(json_data)

            # 每秒钟发送一次数据
            gevent.sleep(1)



    def run(self):
        self.send_system_info()

# WebSocket路由，用于接收WebSocket连接
@app.route('/ws/')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    # 创建并启动WebSocket处理类
    ws_handler = SystemProbeWebSocket(wsock)
    ws_handler.run()

@app.route('/')
@app.route('/index.html')
def index():
    return static_file('index.html', root='.')

if __name__ == '__main__':
    server = WSGIServer(('0.0.0.0', 3000), app,
                        handler_class=WebSocketHandler)
    server.serve_forever()
