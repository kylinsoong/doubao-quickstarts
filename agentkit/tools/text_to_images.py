import os
import sys
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

def text_to_images(prompt, max_images=4, size="2K", model="doubao-seedream-4-5-251128"):
    
    # 从环境变量中获取API Key
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("错误: 请设置环境变量 ARK_API_KEY")
        return []
    
    try:
        # 初始化Ark客户端
        client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=api_key,
        )
        
        print(f"\n正在生成 {max_images} 张图片，提示词: {prompt}")
        print("请稍候...")
        
        # 生成图片
        images_response = client.images.generate(
            model=model,
            prompt=prompt,
            sequential_image_generation="auto",
            sequential_image_generation_options=SequentialImageGenerationOptions(max_images=max_images),
            response_format="url",
            size=size,
            stream=True,
            watermark=False
        )
        
        image_urls = []

        print(f"生成图片响应: {images_response}")
        
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
                    image_urls.append(event.url)
            elif event.type == "image_generation.completed":
                if event.error is None:
                    print("\n图片生成完成!")
                    print(f"使用量: {event.usage}")
        
        return image_urls
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return []

def read_prompts_from_file(file_path):
    """
    从文件中读取提示词，每行一个
    
    参数:
    file_path: 提示词文件路径
    
    返回:
    list: 提示词列表
    """
    prompts = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                stripped_line = line.strip()
                if stripped_line and not stripped_line.startswith('#'):
                    prompts.append(stripped_line)
        return prompts
    except Exception as e:
        print(f"读取提示词文件失败: {str(e)}")
        return []

def main():
    """
    主函数，从当前目录读取prompt.txt并处理所有提示词
    """
    # 从当前目录读取提示词
    current_dir = os.getcwd()
    prompt_file = os.path.join(current_dir, "prompt.txt")
    prompts = read_prompts_from_file(prompt_file)
    
    if not prompts:
        print("错误: 未找到有效的提示词")
        return
    
    print(f"从文件中读取到 {len(prompts)} 个提示词")
    
    # 处理每个提示词
    for i, prompt in enumerate(prompts, 1):
        print(f"\n{'='*60}")
        print(f"处理第 {i} 个提示词:")
        print(f"提示词: {prompt}")
        print(f"{'='*60}")
        
        # 尝试从提示词中提取图片数量
        max_images = 4  # 默认值
        
        # 生成图片
        image_urls = text_to_images(prompt, max_images)

        print(f"生成的图片URL: {image_urls}")
        
        if image_urls:
            # 创建保存目录
            save_dir = os.path.expanduser("~/Downloads/images")
            os.makedirs(save_dir, exist_ok=True)
            
            print("\n生成的图片URL:")
            saved_files = []
            for j, url in enumerate(image_urls, 1):
                print(f"{j}. {url}")
                
                # 下载图片
                file_name = f"{str(uuid.uuid4())}.jpg"
                save_path = os.path.join(save_dir, file_name)
                if download_image(url, save_path):
                    saved_files.append(save_path)
                    print(f"  已保存到: {save_path}")
            
            if saved_files:
                print("\n图片保存完成!")
                print(f"保存目录: {save_dir}")
                print(f"共保存 {len(saved_files)} 张图片")
            else:
                print("\n图片生成成功，但下载失败")
        else:
            print("\n未能生成图片")

if __name__ == "__main__":
    main()
