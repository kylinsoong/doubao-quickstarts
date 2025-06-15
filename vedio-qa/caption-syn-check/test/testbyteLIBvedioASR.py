import os
from byteLIB import ByteVideoASR


appid = os.getenv("X_API_APPID")
access_token = os.getenv("X_API_TOKEN")

print(appid, access_token)

asr = ByteVideoASR(appid=appid, access_token=access_token)

print(asr)

file_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/020.mp4"
result = asr.process(file_url)

print(result)
