import wave

def get_wav_file_length(file_path):
    try:
        with wave.open(file_path, 'rb') as wf:
            # 获取帧数
            frames = wf.getnframes()
            # 获取帧率
            frame_rate = wf.getframerate()
            # 计算时长（秒）
            duration = frames / float(frame_rate)
            return duration
    except FileNotFoundError:
        print("错误: 文件未找到!")
    except Exception as e:
        print(f"错误: 发生了一个未知错误: {e}")
    return None

if __name__ == "__main__":
    length = get_wav_file_length(file_path)
    if length is not None:
        print(f"音频文件时长: {length} 秒")    
