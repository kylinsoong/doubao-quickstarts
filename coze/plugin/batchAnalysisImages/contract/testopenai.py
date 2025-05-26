import re
import io
import os
from openai import OpenAI
import logging



def ark_vision_images(client, item, prompt, endpoint):


    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]
  
    try:
        completion = client.chat.completions.create(
            model=endpoint,
            messages=messages,
            temperature=0.01
        )

        return completion.choices[0].message.content

    except Exception as e:
        logging.error(f"Error while calling the API: {str(e)}")
        return None


def split_frames_into_batches(frames, batch_size):
    if not frames or not isinstance(frames, list):  
        logging.warning("Invalid or empty frames input.")
        return []
    return [frames[i:i + batch_size] for i in range(0, len(frames), batch_size)]


def handler(item, prompt, key, endpoint):
    client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3", api_key=key)
    results = ark_vision_images(client, item, prompt, endpoint)    

    print(results)



images = ["https://pub-kylin.tos-cn-beijing.volces.com/9038/8540f90b4a624b849f39cc8f7a60a457.jpeg","https://pub-kylin.tos-cn-beijing.volces.com/9038/838984caadbc4babb4f5930e08829468.jpeg"]

prompt = """
分析一组图片，提取内容信息，以JSON 格式输出，具体：

1. 合同金额：在第三章 《结算和支付方式》，3.2部分，以人民币符号 ¥开始，以”元“结尾，不包括¥和”元“
2. 合同金额大写：在第三章 《结算和支付方式》，3.2部分，在括号中，以”大写“开头，不包括”大写“
3. 开户行：在第三章 《结算和支付方式》，3.4 部分
4. 账户：在第三章 《结算和支付方式》，3.4 部分，账户长度为21位苏子
5. 户名：在第三章 《结算和支付方式》，3.4 部分

输出结果格式：{"合同金额":<合同金额>, "合同金额大写":<合同金额大写>,"开户行":<开户行>,"账户":<账户>,"户名":<户名>}
"""

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

handler(images, prompt, API_KEY, API_EP_ID)

#ark_vision_images(image_urls)
