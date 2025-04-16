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
    file_path = 'https://sec-kylin.tos-cn-beijing.volces.com/juzi/202503201603-a3692a3e-e8ad-4719-83ab-518f417dae92-.wav?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTZTE0Y2QxZmZhYWI1NDZkYmFiNGY5M2FhYzk2NTk1MmM%2F20250416%2Fcn-beijing%2Ftos%2Frequest&X-Tos-Date=20250416T114658Z&X-Tos-Expires=3600&X-Tos-SignedHeaders=host&X-Tos-Signature=18d0e9a24c71101a6e43cb9e0125ea8f0d686654e9bea5d637ed60f68b48fa2a'
    length = get_wav_file_length(file_path)
    if length is not None:
        print(f"音频文件时长: {length} 秒")    
