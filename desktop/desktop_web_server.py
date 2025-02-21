import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import threading

def start_web_server():
    """启动本地网站服务器"""
    def run_server():
        # 获取当前文件的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建dist目录的绝对路径
        dist_path = os.path.join(os.path.dirname(current_dir), 'origin-chat', 'dist')
        
        app = FastAPI()
        # 挂载静态文件目录
        app.mount("/", StaticFiles(directory=dist_path, html=True), name="static")
        
        # 启动服务器
        uvicorn.run(app, host="localhost", port=8777)
            
    # 在新线程中启动服务器
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
