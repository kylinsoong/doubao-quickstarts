from openai import OpenAI

model_url = "https://ark.cn-beijing.volces.com/api/v3"

class ByteLLM:
    """
    自定义 LLM 类，使用 OpenRouter API 来生成回复
    """
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key

    def generate(self, messages):
        """
        发送对话消息给大模型

        参数:
            messages: 一个 list，每个元素都是形如 {'role': role, 'content': content} 的字典

        返回:
            LLM 返回的回复文本
        """
        client = OpenAI(
            # 此为默认路径，您可根据业务所在地域进行配置
            base_url=model_url,
            # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
            api_key=self.api_key,
        )

        response = client.chat.completions.create(
            # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
            model=self.model,
            messages=messages
        )


        # 提取 LLM 响应文本
        try:
            content = response.choices[0].message
            return content
        except KeyError:
            raise Exception("大模型返回错误")