import requests
import wave
import contextlib
import io

url = "https://haier-poc.tos-cn-shanghai.volces.com/haier/881311_20250618100738066.wav"

response = requests.get(url, stream=True)
response.raise_for_status()  # Ensure the request was successful

with io.BytesIO(response.content) as wav_buffer:
    with contextlib.closing(wave.open(wav_buffer, 'rb')) as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        print(f"Duration: {duration:.2f} seconds")

