#!/usr/bin/env python3

import os
from openai import OpenAI

def ark_vision_images(client, API_EP_ID, item, prompt, temperature):
    messages = [
        {"role": "user", "content": [{"type": "text", "text": prompt}] + [
            {"type": "image_url", "image_url": {"url": url}} for url in item
        ]}
    ]
    try:
        completion = client.chat.completions.create(
            model=API_EP_ID,
            messages=messages,
            thinking = {
                "type":"disabled"
            },
            temperature=temperature
        )
        return completion.choices[0].message.content, completion.usage
    except Exception as e:
        return str(e)

def main():
    parser = argparse.ArgumentParser(description='Process ARK API parameters and images.')
    parser.add_argument('--ARK_API_KEY', type=str, required=True, help='ARK API Key')
    parser.add_argument('--ARK_API_ENGPOINT_ID', type=str, required=True, help='ARK API Endpoint ID')
    parser.add_argument('--images', nargs='+', required=True, help='List of image URLs')

    args = parser.parse_args()

    API_KEY = args.ARK_API_KEY
    API_EP_ID = args.ARK_API_ENGPOINT_ID
    images = args.images

    client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3",api_key=API_KEY)

    prompt = """
你的任务是分析一组图片，分析结果将用于贷款授信。你需要仔细观察图片，分析图片中人的风险控制要素。

请从分析图片，提取如下风控要素：
1. 性别: 明确判断图片中人的性别，只能填写“男”或“女”。
2. 年龄: 精准判断图片中人的年龄，以年龄段形式呈现，例如“30-35”“35-40”等。
3. 表情: 清晰、准确地描述图片中人的表情。
4. 职业: 根据图片特征判断照片中人的职业，若在办公室环境，判定为白领；若有其他明显特征可明确职业，则如实填写；若难以判断，填写“无法判断”。
5. 背景: 详细阐述背景情况，尽可能准确判断可能的地点，如公司、工厂、室外等。同时，说明背景中是否有人，若有人，详细描述其动作。
6. 戴眼镜: 明确判断图片中人是否戴眼镜，只能填写“是”或“否”。
7. 戴耳机: 明确判断图片中人是否戴耳机，只能填写“是”或“否”。
8. 戴口罩: 明确判断图片中人是否戴口罩，只能填写“是”或“否”。
9. 头发长短: 描述图片中人头发的长短情况，例如长发、短发等。
10. 背包: 明确判断图片中人是否背包，只能填写“是”或“否”
11. 敷面膜: 明确判断图片中人是否敷面膜，只能填写“是”或“否”
12. 戴帽子: 明确判断图片中人是否戴帽子，只能填写“是”或“否”
13. 戴大金链子: 明确判断图片中人是否戴大金链子，只能填写“是”或“否”
14. 金融字样: 明确判断图片中是否有“贷”、”信贷“、“银行”，“贷款”，“征信”，“融资”，“签约”，“咨询”，“企业”等金融相关字样，只能填写“是”或“否”
15. 锦旗: 明确判断图片中是否有锦旗，只能填写“是”或“否”
16. 方格吊顶: 明确判断图片中是否有方格吊顶，只能填写“是”或“否”
17. 室内绿植盆景: 明确判断图片中是否有室内绿植、盆景，只能填写“是”或“否”
18. 百叶窗: 明确判断图片中是否有百叶窗，只能填写“是”或“否”
19. 玻璃墙: 明确判断图片中是否有玻璃墙，只能填写“是”或“否”
20. 海报: 明确判断图片中是否有海报，只能填写“是”或“否”
21. 双层床: 明确判断图片中是否有双层床、高低床，只能填写“是”或“否”
22. 疑似医疗场景: 明确判断图片中是否医疗场景，比如医院字样、病床、穿着病人服等，只能填写“是”或“否”
23. 赌场场景: 明确判断图片中是否赌博场景，只能填写“是”或“否”
24. 他人入境1: 明确判断图片中是否有他人入境，只能填写“是”或“否”
25. 他人入境2: 明确判断图片中是否有他人入境（排除怀抱幼儿），只能填写“是”或“否”
26. 其他几个人入境: 明确判断图片中是否有他人入境，有的话填写入境人数
27. 有几只手: 明确判断图片中有几只手
28. 人员状态: 描述图片中人的站立状态，如坐着、站着、躺着
29. 经营场所: 描述图片中的场景是什么经营场景，比如超市、服装店、建材店、餐饮店等
30. 工作服: 明确判断图片中是否有工作服、工作帽子，并描述是哪种职业类型，比如建筑工人、外卖员、快递员、保安等
31. 公安: 明确判断图片中是否有“公安”字样，只能填写“是”或“否”
32. 律师: 明确判断图片中是否有“律师”字样，只能填写“是”或“否”
33. 检查官: 明确判断图片中是否有“检查官”字样，只能填写“是”或“否”
34. 法官: 明确判断图片中是否有“法官”字样，只能填写“是”或“否”
35. 学生: 明确判断图片中是否有“学校”、“学院”等字样，只能填写“是”或“否”
36. 是否活人: 明确判断图片中人是否是活人，只能填写“是”或“否”。
37. 是否他人拍照: 明确判断图片中人是否由他人帮助拍照扫脸，只能填写“是”或“否”。
38. 是否被胁迫: 明确判断图片中人是否有被他人胁迫，只能填写“是”或“否”
39. 是否直视镜头: 明确判断图片中人是否直视镜头，只能填写“是”或“否”
40. 是否屏拍: 明确判断图片中人是否直接拍摄所得，如果是直接拍的填写“否”，如果识别到拍摄的人在画框中、手机中就填写“是”
41. 是否水印: 明确判断图片中是否有水印，只能填写“是”或“否”
42. 脸部是否有遮挡: 明确判断图片中人的脸部是否被遮挡，只能填写“是”或“否”
43. 眼皮是否有遮挡: 明确判断图片中人的眼皮是否被遮挡，只能填写“是”或“否”
44. 残疾: 明确判断图片中人是否残疾，只能填写“是”或“否”
45. 纹身: 明确判断图片中人是否有纹身，只能填写“有”或“无”
46. 裸露身体: 明确判断图片中人是否裸露身体，只能填写“是”或“否”
47. 是否闭眼: 明确判断图片中人是否有一只或两只眼睛闭着，只能填写“是”或“否”
48. 是否在车内: 判断图片中人是否在车内，只能填写“是”或“否”。
49. 是否光头: 明确判断图片中人是否光头，只能填写“是”或“否”
50. 场景类型: 描述图片中所在的场景类型，比如办公环境、卧室、医院、车内、马路、建筑工地等
51. 黑产字样: 明确判断图片中是否有“法务”、“法律”、“债务”、“信用管理”、“信用服务”、“征信”、“信用修复”、“账单规划”、“催收”、“监管”、“信访”等相关字样，只能填写“是”或“否”
52. 白墙: 明确判断图片中是否为白墙，只能填写“是”或“否”

以JSON格式输出分析结果，格式如下(如果照片中没有人脸，则输出对应的note提示)：
[
{
  "基础特征": {
    "性别": "",
    "年龄": "",
    "头发长短": "",
    "是否活人": "",
    "是否闭眼": "",
    "是否光头": "",
    "有几只手": "",
    "人员状态": "",
    "裸露身体": "",
    "残疾": ""
  },
  "穿戴特征": {
    "戴眼镜": "",
    "戴耳机": "",
    "戴口罩": "",
    "背包": "",
    "敷面膜": "",
    "戴帽子": "",
    "戴大金链子": "",
    "纹身": ""
  },
  "场景特征": {
    "背景": "",
    "方格吊顶": "",
    "室内绿植盆景": "",
    "百叶窗": "",
    "玻璃墙": "",
    "海报": "",
    "双层床": "",
    "疑似医疗场景": "",
    "赌场场景": "",
    "是否在车内": "",
    "场景类型": "",
    "经营场所": "",
    "金融字样": "",
    "锦旗": "",
    "是否水印": "",
    "黑产字样": "",
    "白墙": ""
  },
  "职业特征": {
    "职业": "",
    "工作服": "",
    "公安": "",
    "律师": "",
    "检查官": "",
    "法官": "",
    "学生": ""
  },
  "胁迫或他拍特征": {
    "是否他人拍照": "",
    "是否被胁迫": "",
    "是否屏拍": "",
    "他人入境1": "",
    "他人入境2": "",
    "其他几个人入境": ""
  },
  "微表情特征": {
    "表情": "",
    "是否直视镜头": "",
    "脸部是否有遮挡": "",
    "眼皮是否有遮挡": ""
  }
},
// 更多的照片的分析

// 如果照片中没有人脸，则输出 {"note": "照片中没有人脸"}
]

"""

    results = ark_vision_images(client, API_EP_ID, images, prompt, 0.01)

    print(results[0])
    print(results[1])
 

if __name__ == "__main__":
    main()
