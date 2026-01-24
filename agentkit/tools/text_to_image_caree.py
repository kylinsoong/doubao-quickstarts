import os
import requests
import uuid
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions

def download_image(url, save_path):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"下载图片失败: {str(e)}")
        return False

def generate_image(prompt, model="doubao-seedream-4-5-251128", size="2K"):
    # 从环境变量中获取API Key
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 ARK_API_KEY")
        return None
    
    try:
        # 初始化Ark客户端
        client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=api_key,
        )
        
        print(f"\n正在生成图片，提示词: {prompt}")
        print("请稍候...")
        
        # 生成图片
        images_response = client.images.generate(
            model=model,
            prompt=prompt,
            response_format="url",
            size=size,
            stream=True,
            watermark=False
        )
        
        image_url = None
        
        # 处理流式响应
        for event in images_response:
            if event is None:
                continue
            if event.type == "image_generation.partial_failed":
                print(f"生成图片失败: {event.error}")
                break
            elif event.type == "image_generation.partial_succeeded":
                if event.error is None and event.url:
                    print(f"生成成功: {event.url}")
                    image_url = event.url
            elif event.type == "image_generation.completed":
                if event.error is None:
                    print("\n图片生成完成!")
                    print(f"使用量: {event.usage}")
        
        return image_url
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

def main():
    """
    主函数，生成单个图片
    """
    # 提示词
    prompt = """
目标 / 风格：
呈现专业、自信且充满目标感的形象
组合公式：
专业穿搭 + 工作环境 + 自信表情 + 窗边自然光
提示词：
一位自信的少女坐在现代办公室环境中，穿着专业服装，桌上放着笔记本电脑，窗边洒入柔和日光，展现有企图心的神情，营造生产力美感、职业导向氛围，采用干净构图。
    """
    
    # 生成图片
    image_url = generate_image(prompt)
    
    if image_url:
        # 创建保存目录
        save_dir = os.path.expanduser("~/Downloads/images")
        os.makedirs(save_dir, exist_ok=True)
        
        # 下载图片
        file_name = f"feature_{str(uuid.uuid4())}.jpg"
        save_path = os.path.join(save_dir, file_name)
        if download_image(image_url, save_path):
            print(f"\n图片保存成功!")
            print(f"保存路径: {save_path}")
        else:
            print("\n图片生成成功，但下载失败")
    else:
        print("\n未能生成图片")

if __name__ == "__main__":
    main()
