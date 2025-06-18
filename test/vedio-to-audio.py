import os
import argparse
from moviepy.editor import VideoFileClip
from pathlib import Path

os.environ["FFMPEG_BINARY"] = "/opt/homebrew/bin/ffmpeg" 

def convert_video_to_audio(video_path, output_dir=None, audio_format="mp3", bitrate="192k", codec=None):
    """
    将视频文件转换为音频文件
    
    参数:
        video_path (str): 输入视频文件的路径
        output_dir (str, optional): 输出音频文件的目录。默认为None，表示与输入视频相同的目录。
        audio_format (str, optional): 输出音频格式。默认为"mp3"。
        bitrate (str, optional): 音频比特率，例如"192k"。默认为"192k"。
        codec (str, optional): 音频编解码器。默认为None，由moviepy自动选择。
    
    返回:
        str: 输出音频文件的路径
    """
    try:
        # 确保视频文件存在
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"视频文件不存在: {video_path}")
        
        # 获取视频文件名（不带扩展名）
        video_file_name = os.path.basename(video_path)
        video_name, _ = os.path.splitext(video_file_name)
        
        # 确定输出目录
        if output_dir is None:
            output_dir = os.path.dirname(video_path)
        else:
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
        
        # 构建输出音频文件路径
        output_audio_path = os.path.join(output_dir, f"{video_name}.{audio_format}")
        
        # 加载视频文件
        video_clip = VideoFileClip(video_path)
        
        # 提取音频
        audio_clip = video_clip.audio
        
        # 保存音频
        audio_clip.write_audiofile(
            output_audio_path,
            bitrate=bitrate,
            codec=codec
        )
        
        # 关闭剪辑对象以释放资源
        audio_clip.close()
        video_clip.close()
        
        return output_audio_path
    
    except Exception as e:
        print(f"转换过程中出错: {e}")
        return None

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="将视频文件转换为音频文件")
    
    # 添加必需的参数
    parser.add_argument("video_path", help="输入视频文件的路径")
    
    # 添加可选参数
    parser.add_argument("-o", "--output_dir", help="输出音频文件的目录")
    parser.add_argument("-f", "--format", default="mp3", choices=["mp3", "wav", "ogg", "m4a"], help="输出音频格式")
    parser.add_argument("-b", "--bitrate", default="192k", help="音频比特率，例如'192k'")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 调用转换函数
    output_path = convert_video_to_audio(
        args.video_path,
        args.output_dir,
        args.format,
        args.bitrate
    )
    
    if output_path:
        print(f"成功转换视频为音频: {output_path}")
    else:
        print("转换失败")

if __name__ == "__main__":
    main()    
