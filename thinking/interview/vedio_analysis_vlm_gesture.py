import os
import json
from volcenginesdkarkruntime import Ark
import time

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

original_prompt ="""
你是一名HR助手，分析面试视频，给面试人进行六维度打标。具体任务是分析面试的表情、样貌、手势、姿势、以及语言进行六维度打标。

具体：
1. 表情、样貌、手势、姿势通过分析视频中图像获取
2. 语言通过<ASR_JSON_subtitles>部分的对话获取如下ASR 字幕示例，字幕 "展现自己的价值" 开始时间是 165.16 秒，结束的时间是 166.54 秒。 

<ASR 字幕示例>
  {
    "start_time": 165.16,
    "end_time": 166.54,
    "text": "展现自己的价值"
  }
</ASR 字幕示例>

## ASR_JSON_subtitles

<ASR_JSON_subtitles>
{{ASR_JSON_SUBTITLES}}
</ASR_JSON_subtitles>

## 六维度打标规则

六个维度分别为：情绪稳定性与抗压能力、沟通意愿与表达能力、性格特质与岗位适配性、诚信度与心理状态、职业素养与细节意识、对岗位的认知与兴趣。每个维度有四个标签，每个标签有对应的判断依据，需要对六个维度进行唯一打标签，并简要描述原因，即为什么打此标签。

### 情绪稳定性与抗压能力

1. 情绪稳定
   - 判断依据：面对压力问题时，眼神镇定（无频繁眨眼或躲闪），面部肌肉放松（嘴角无抽搐），坐姿保持端正（无突然后倾或僵硬）。
2. 抗压性强
   - 判断依据：被追问时，手势自然（如手部动作不急促），身体微微前倾（主动回应而非防御），声调平稳无明显起伏。
3. 易紧张
   - 判断依据：回答时频繁摸头发、搓手，膝盖轻微抖动，眼神快速扫视四周，面部表情僵硬（如笑容不自然）。
4. 情绪波动大
   - 判断依据：被否定时，瞬间皱眉或撇嘴，身体突然后靠并抱臂，语气带明显急躁（如语速突然加快）。

### 沟通意愿与表达能力

1. 积极沟通
   - 判断依据：主动保持眼神交流（每次对视超 3 秒），说话时点头回应面试官，手势与语言内容匹配（如用手势强调重点）。
2. 善于表达
   - 判断依据：讲述时眉飞色舞，身体自然前倾，手势丰富且不夸张（如用手掌比划数据逻辑），表情随内容变化（如谈到成就时微笑）。
3. 沟通被动
   - 判断依据：眼神多数时间看向桌面，回答简短（仅 “是”“否”），身体后靠且双手放于腿上，无主动肢体互动。
4. 表达障碍
   - 判断依据：说话时频繁摸鼻子、舔嘴唇，手势僵硬（如双手紧握不放），身体侧对面试官，表情与内容矛盾（如说 “自信” 时眼神躲闪）。

### 性格特质与岗位适配性

1. 外向亲和
   - 判断依据：进门时微笑点头，坐姿舒展（如手臂自然放于桌面），说话时嘴角上扬，主动与面试官有肢体呼应（如递资料时双手接拿）。
2. 严谨自信
   - 判断依据：坐姿笔挺（腰背挺直），手势稳重（无频繁小动作），眼神坚定（直视面试官），回答时条理清晰（如用手势比划 “第一、第二”）。
3. 内向谨慎
   - 判断依据：坐姿拘谨（身体前倾不足 15°），手势少且幅度小，说话声音偏低，表情较少（如全程面无微笑）。
4. 浮躁随意
   - 判断依据：抖腿、转笔等小动作频繁，坐姿东倒西歪，手势夸张且无逻辑（如随意挥舞手臂），眼神飘忽不定。

### 诚信度与心理状态

1. 真诚坦诚
   - 判断依据：回答时眼神稳定，身体朝向面试官，手势开放（如手掌向上表达观点），语言与肢体动作一致（如说 “认同” 时点头）。
2. 有所掩饰
   - 判断依据：被问及敏感问题时，突然摸脖子、眨眼频率变高，身体不自觉后移，手势遮挡面部（如手捂嘴或摸鼻子）。
3. 自信笃定
   - 判断依据：说话时头部微微上扬，手势有力（如握拳强调重点），身体前倾且肩膀放松，眼神直视不回避。
4. 心虚回避
   - 判断依据：回答时频繁低头看手，身体侧转（如肩膀偏向一侧），用 “嗯”“呃” 等语气词拖延时间，手势僵硬地放在腿上。


### 职业素养与细节意识

1. 礼仪规范
   - 判断依据：进门敲门轻缓（3 声间隔均匀），就座后双手自然放于桌面，递资料时双手奉上，离开时主动整理座椅。
2. 细节关注
   - 判断依据：注意到面试官递来的资料边角，会用手扶正；坐下前观察座椅位置，调整到合适距离；回答时注意用语礼貌（如 “谢谢面试官的提问”）。
3. 随意散漫
   - 判断依据：进门不敲门或大力推门，就座后翘二郎腿，单手接拿资料，身体靠在椅背上超过 1/2 椅背。
4. 礼仪欠缺
   - 判断依据：坐下时双腿张开超过肩宽，说话时手指指向面试官，离开时未整理桌面物品，眼神不关注面试官动作（如递水时无回应）。

### 对岗位的认知与兴趣

1. 高度匹配
   - 判断依据：谈论岗位核心职责时，身体前倾超 30°，眼神发亮，手势主动指向简历中相关经历，语气带兴奋感（如声调提高）。
2. 准备充分
   - 判断依据：回答时引用岗位 JD 关键词，手势配合列举技能（如 “我具备三点优势”），表情专注（无东张西望），主动询问岗位细节。
3. 兴趣不足
   - 判断依据：谈及岗位时，身体后靠且手臂交叉，眼神看向别处，回答简短（如 “了解一点”），手势少且无活力。
4. 认知模糊
   - 判断依据：被问及岗位理解时，频繁摸头、眼神迷茫，手势无指向性（如双手乱晃），身体左右转动（似在寻找答案），回答与岗位需求脱节。


# 输出格式
以结构化 JSON 格式输出，不做额外的解释。
输出示例：
{"情绪稳定性与抗压能力":{"tag":<str>,"reason":<str>},"沟通意愿与表达能力":{"tag":<str>,"reason":<str>},"性格特质与岗位适配性":{"tag":<str>,"reason":<str>},"诚信度与心理状态":{"tag":<str>,"reason":<str>},"职业素养与细节意识":{"tag":<str>,"reason":<str>},"对岗位的认知与兴趣":{"tag":<str>,"reason":<str>}}

"""

def analyze_video(video_url: str):
    if not API_KEY or not API_EP_ID:
        raise ValueError("Missing ARK_API_KEY or ARK_API_ENGPOINT_ID environment variables")

    with open("asr.json", 'r', encoding='utf-8') as file:
        collection_dialog = json.load(file)

    prompt = original_prompt.replace("{{ASR_JSON_SUBTITLES}}", json.dumps(collection_dialog, ensure_ascii=False))


    client = Ark(api_key=API_KEY)
    
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "video_url",
                        "video_url": {
                            "url": video_url,
                            "fps": 0.5,
                            "detail": "low"
                        }
                    },
                ],
            }
        ],
        thinking = {
            "type":"disabled"
        }
    )

    return completion.choices[0].message.content, completion.usage

@log_time
def main():
    video_url = "https://pub-kylin.tos-cn-beijing.volces.com/0001/201.mov"
    summary, usage = analyze_video(video_url)
    #print(summary)
    json_obj = json.loads(summary)
    with open("vlm.json", 'w') as file:
        json.dump(json_obj, file, ensure_ascii=False)
    print(usage)


if __name__ == "__main__":
    main()

