import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

TIP = "提供参考内容"

prompt = """
请参考如下文档，回答用户问题：

###
人工智能在医疗领域已经有了广泛的应用。其中，医学影像诊断是一个重要的方面。人工智能算法可以对X光、CT、MRI等医学影像进行分析，帮助医生更准确地检测疾病，如肺癌、乳腺癌等。
在药物研发方面，人工智能可以加速药物的筛选和研发过程。通过对大量的生物数据和化合物信息进行分析，人工智能可以预测药物的有效性和安全性，从而减少研发时间和成本。
另外，智能健康监测设备也是人工智能在医疗领域的应用之一。这些设备可以实时监测患者的生命体征，如心率、血压、血糖等，并将数据传输到医疗系统中，以便医生及时进行干预和治疗。
###

问题：人工智能在医疗领域的主要应用有哪些？
"""

def main():
    client = Ark(api_key=API_KEY)
    print("==>", TIP)
    print("<PROMPT>: ", prompt)
    print("<RESPONSE>: ")
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    print(completion.choices[0].message.content)

    print(completion.usage)

if __name__ == "__main__":
    main()
