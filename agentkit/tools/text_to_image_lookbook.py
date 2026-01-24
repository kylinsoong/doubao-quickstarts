import os
import requests
import uuid
from volcenginesdkarkruntime import Ark
from volcenginesdkarkruntime.types.images.images import SequentialImageGenerationOptions

def download_image(url, save_path):
    """
    下载图片并保存到指定路径
    
    参数:
    url: 图片URL
    save_path: 保存路径
    
    返回:
    bool: 下载是否成功
    """
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
    """
    根据提示词生成图片
    
    参数:
    prompt: 图片生成提示词
    model: 使用的模型，默认"doubao-seedream-4-5-251128"
    size: 图片尺寸，默认"2K"
    
    返回:
    str: 生成的图片URL
    """
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
#目标／风格：  
如同时尚型录般精致的穿搭照片  

#组合公式：  
全身姿势 + 时尚穿搭 + 编辑感构图 + 干净背景 + 风格化打光  

#提示词：  
一张编辑风全身时尚照，女生身穿西式街头风穿搭，站在现代城市步道上，柔和阴影、杂志感构图、时尚型录版面、干净粉彩色调、时尚姿势、高解析度画面。
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
