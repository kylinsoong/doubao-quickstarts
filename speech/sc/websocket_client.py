import asyncio
import websockets
import uuid
import json
import yaml
import argparse
import wave
import time
import os
import threading

class WebSocketClient:
    def __init__(self, config_path="config.yaml"):
        # 加载配置文件
        _, ext = os.path.splitext(config_path)
        with open(config_path, "r") as f:
            if ext.lower() in [".yaml", ".yml"]:
                self.config = yaml.safe_load(f)
            else:
                self.config = json.load(f)
        
        # 从环境变量读取配置，优先级高于配置文件
        self.config["app_id"] = os.environ.get("APP_ID", self.config.get("app_id"))
        self.config["access_key"] = os.environ.get("ACCESS_KEY", self.config.get("access_key"))
        self.config["app_key"] = os.environ.get("APP_KEY", self.config.get("app_key"))
        
        self.uri = self.config["websocket_url"]
        self.connect_id = str(uuid.uuid4())
        self.websocket = None
        self.is_connected = False
        self.audio_file = None
        self.audio_stream = None
        
    def configure(self, app_id=None, access_key=None, app_key=None):
        """配置客户端参数"""
        if app_id:
            self.config["app_id"] = app_id
        if access_key:
            self.config["access_key"] = access_key
        if app_key:
            self.config["app_key"] = app_key
    
    def get_headers(self):
        """生成请求头"""
        return {
            "X-Api-App-ID": self.config["app_id"],
            "X-Api-Access-Key": self.config["access_key"],
            "X-Api-Resource-Id": self.config["resource_id"],
            "X-Api-App-Key": self.config["app_key"],
            "X-Api-Connect-Id": self.connect_id
        }
    
    async def connect(self):
        """建立 WebSocket 连接"""
        try:
            self.websocket = await websockets.connect(
                self.uri,
                extra_headers=self.get_headers()
            )
            self.is_connected = True
            print(f"WebSocket 连接已建立")
            print(f"连接 ID: {self.connect_id}")
            
            # 启动消息接收线程
            asyncio.create_task(self.receive_messages())
            
        except Exception as e:
            print(f"WebSocket 连接错误: {e}")
            self.is_connected = False
    
    async def receive_messages(self):
        """接收并处理消息"""
        try:
            while self.is_connected:
                message = await self.websocket.recv()
                await self.handle_message(message)
        except websockets.exceptions.ConnectionClosed as e:
            print(f"WebSocket 连接已关闭: {e}")
            self.is_connected = False
        except Exception as e:
            print(f"接收消息错误: {e}")
            self.is_connected = False
    
    async def handle_message(self, message):
        """处理收到的消息"""
        try:
            # 尝试解析 JSON 消息
            data = json.loads(message)
            print(f"收到 JSON 消息: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 根据消息类型进行不同处理
            message_type = data.get("type", "")
            if message_type == "audio":
                # 处理音频响应
                audio_data = data.get("data", "")
                print(f"收到音频数据，长度: {len(audio_data)}")
            elif message_type == "text":
                # 处理文本响应
                text = data.get("text", "")
                print(f"收到文本响应: {text}")
            elif message_type == "status":
                # 处理状态消息
                status = data.get("status", "")
                print(f"收到状态消息: {status}")
            else:
                # 处理其他类型消息
                print(f"收到未知类型消息: {message_type}")
                
        except json.JSONDecodeError:
            # 如果不是 JSON 格式，直接打印
            print(f"收到非 JSON 消息: {message}")
    
    async def send_audio_file(self, file_path, chunk_size=8000, sample_rate=16000):
        """发送音频文件"""
        if not self.is_connected:
            print("WebSocket 未连接，无法发送音频")
            return
        
        try:
            # 打开音频文件
            with wave.open(file_path, "rb") as wf:
                # 检查音频格式
                if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != sample_rate:
                    print(f"音频格式要求: 单声道, 16位, {sample_rate}Hz")
                    print(f"当前音频: {wf.getnchannels()}声道, {wf.getsampwidth()*8}位, {wf.getframerate()}Hz")
                    return
                
                print(f"开始发送音频文件: {file_path}")
                
                # 发送音频数据
                while True:
                    data = wf.readframes(chunk_size)
                    if not data:
                        break
                    
                    # 构建音频消息
                    audio_message = {
                        "type": "audio",
                        "data": data.hex(),  # 将音频数据转换为十六进制字符串
                        "timestamp": int(time.time() * 1000),
                        "sample_rate": sample_rate,
                        "chunk_size": len(data)
                    }
                    
                    # 发送消息
                    await self.websocket.send(json.dumps(audio_message))
                    
                    # 控制发送速率
                    await asyncio.sleep(chunk_size / sample_rate)
                
                print("音频文件发送完成")
                
        except Exception as e:
            print(f"发送音频文件错误: {e}")
    
    async def send_text(self, text):
        """发送文本消息"""
        if not self.is_connected:
            print("WebSocket 未连接，无法发送文本")
            return
        
        try:
            # 构建文本消息
            text_message = {
                "type": "text",
                "text": text,
                "timestamp": int(time.time() * 1000)
            }
            
            # 发送消息
            await self.websocket.send(json.dumps(text_message))
            print(f"已发送文本消息: {text}")
            
        except Exception as e:
            print(f"发送文本消息错误: {e}")
    
    async def disconnect(self):
        """断开 WebSocket 连接"""
        if self.is_connected:
            try:
                await self.websocket.close()
                self.is_connected = False
                print("WebSocket 连接已断开")
            except Exception as e:
                print(f"断开连接错误: {e}")

async def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="WebSocket 客户端")
    parser.add_argument("--config", type=str, default="config.yaml", help="配置文件路径")
    parser.add_argument("--app-id", type=str, help="APP ID")
    parser.add_argument("--access-key", type=str, help="Access Key")
    parser.add_argument("--app-key", type=str, help="App Key")
    parser.add_argument("--audio-file", type=str, help="要发送的音频文件路径")
    parser.add_argument("--text", type=str, help="要发送的文本消息")
    args = parser.parse_args()
    
    # 创建客户端实例
    client = WebSocketClient(args.config)
    
    # 配置客户端
    client.configure(
        app_id=args.app_id,
        access_key=args.access_key,
        app_key=args.app_key
    )
    
    try:
        # 建立连接
        await client.connect()
        
        # 如果有音频文件，发送音频
        if args.audio_file:
            await client.send_audio_file(args.audio_file)
        
        # 如果有文本消息，发送文本
        if args.text:
            await client.send_text(args.text)
        
        # 保持运行，直到用户中断
        print("客户端正在运行，按 Ctrl+C 停止")
        while client.is_connected:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("客户端正在停止...")
    finally:
        # 断开连接
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())