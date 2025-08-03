import requests
import wave
import contextlib
import io

url = "https://haier-poc.tos-cn-shanghai.volces.com/haier/881311_20250618100738066.wav?X-Tos-Algorithm=TOS4-HMAC-SHA256&X-Tos-Credential=AKLTYWNjMDE4OTAyNzBmNGE1Nzg3YjEzMmFiY2UxMmViYTY%2F20250803%2Fcn-shanghai%2Ftos%2Frequest&X-Tos-Date=20250803T021847Z&X-Tos-Expires=3600&X-Tos-SignedHeaders=host&X-Tos-Signature=1f4f65427e3085bd666774c8e42f4338f04e479e35a48e3caddacdb60fb46b34"

response = requests.get(url, stream=True)
response.raise_for_status()  # Ensure the request was successful

with io.BytesIO(response.content) as wav_buffer:
    with contextlib.closing(wave.open(wav_buffer, 'rb')) as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        print(f"Duration: {duration:.2f} seconds")

