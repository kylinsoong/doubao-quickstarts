import os
import json
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

TIP = "限制模型输出格式"


prompt = """请提取参考资料中的所有病症，并且以json格式返回。
回答满足下面的格式要求：
1、以json的格式返回答案，json只包括一个key, key="disease"，对应的值为列表，存储参考资料中的病症。

参考资料：
失眠在《内经》中称为“目不瞑”、“不得眠”、“不得卧”，其原因主要有两种：一是其他病症影响，如咳嗽、呕吐、腹满等，使人不得安卧；二是气血阴阳失和，使人不能入寐。中医常用
养心安神的方法治疗失眠,既可治标、又可治本,还可以避免西药安眠药容易成瘾的弊端。中医认为，失眠多因脏腑阴阳失调，气血失和所致。正如《灵枢大惑论》中记载：“卫气不得入>于阴，常留于阳，留于阳则气满；阳气满则阳娇盛，不得入于阴则阴气虚，故目不瞑矣。”在临床上，治疗失眠应着重调理脏腑及气血阴阳，以“补其不足，泻其有余，调其虚实”，可采>取补益心脾、滋阴降火、交通心肾、疏肝养血、益气镇惊、活血通络等治法，使气血和畅，阴阳平衡，脏腑功能恢复正常。
"""

system_message = {
    "role": "system",
    "content": "你需要严格按照用户的格式要求返回答案。"
}
user_message = {
    "role": "user",
    "content": prompt
}

messages = [system_message, user_message]

def main():
    print("==>", TIP)

    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=messages
    )

    response_content = completion.choices[0].message.content
    result = json.loads(response_content)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print(completion.usage)


if __name__ == "__main__":
    main()
