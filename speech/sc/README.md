# WebSocket 客户端使用说明

这是一个用于连接到字节跳动实时语音大模型 API 的 WebSocket 客户端。

## 功能特性

- 支持通过 WebSocket 连接到实时语音大模型 API
- 支持发送音频文件（WAV 格式）
- 支持发送文本消息
- 支持配置文件和命令行参数
- 自动处理不同类型的响应消息

## 安装依赖

```bash
pip install websockets
```

## 配置文件

客户端现在支持 YAML 格式的配置文件，默认使用 `config.yaml`。

创建 `config.yaml` 文件，配置以下参数：

```yaml
websocket_url: wss://openspeech.bytedance.com/api/v3/realtime/dialogue
app_id: "your-app-id"
access_key: "your-access-key"
resource_id: volc.speech.dialog
app_key: PlgVMyYm7fT3QnU6
```

参数说明：
- `websocket_url`: WebSocket 服务器地址
- `app_id`: 从火山引擎控制台获取的 APP ID
- `access_key`: 从火山引擎控制台获取的 Access Token
- `resource_id`: 固定值，无需修改
- `app_key`: 固定值，无需修改

## 环境变量支持

客户端支持从环境变量读取以下配置参数，优先级高于配置文件：

- `APP_ID`: 应用 ID
- `ACCESS_KEY`: 访问密钥
- `APP_KEY`: 应用密钥

例如：

```bash
export APP_ID="your-app-id"
export ACCESS_KEY="your-access-key"
export APP_KEY="your-app-key"
python websocket_client.py
```

## 使用方法

### 基本用法

```bash
python websocket_client.py
```

### 指定配置文件

```bash
python websocket_client.py --config my_config.json
```

### 通过命令行指定参数

```bash
python websocket_client.py --app-id your-app-id --access-key your-access-key --app-key your-app-key
```

### 发送音频文件

```bash
python websocket_client.py --audio-file test.wav
```

注意：音频文件必须是单声道、16位、16kHz 采样率的 WAV 格式。

### 发送文本消息

```bash
python websocket_client.py --text "你好，我是 WebSocket 客户端"
```

### 组合使用

```bash
python websocket_client.py --app-id your-app-id --access-key your-access-key --audio-file test.wav --text "你好"
```

## 代码结构

- `websocket_client.py`: 主客户端代码
- `config.json`: 配置文件
- `README.md`: 使用说明

## 注意事项

1. 请确保从火山引擎控制台获取正确的 APP ID 和 Access Token
2. 音频文件必须符合要求的格式
3. 连接过程中可能会遇到网络问题，请确保网络稳定
4. 客户端会自动处理连接断开和错误情况

## 示例输出

```
WebSocket 连接已建立
连接 ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
开始发送音频文件: test.wav
音频文件发送完成
客户端正在运行，按 Ctrl+C 停止
```

## 错误处理

客户端会自动处理以下错误：
- 连接失败
- 连接断开
- 消息接收错误
- 音频文件格式错误
- 发送消息错误

当遇到错误时，客户端会打印详细的错误信息，并尝试优雅地处理。

## 扩展功能

可以根据需要扩展以下功能：
- 添加音频流录制功能
- 实现更复杂的消息处理逻辑
- 添加日志记录功能
- 支持更多音频格式
- 实现重连机制

## 许可证

MIT License