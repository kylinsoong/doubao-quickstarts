import os
import json
import logging
import time
from volcenginesdkarkruntime import Ark
from concurrent.futures import ThreadPoolExecutor
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

original_prompt = """
你是一位催收质检管理员，你的任务是仔细分析提供的JSON结构化客服与客户对话，根据「异常发生判断标准」检测是否发生异常、异常总结、异常发生的责任方、客服是否保持平静、异常类型、相关对话、处理建议。
以下是异常发生判断标准：
<exception_criteria>
## 异常发生判断标准
如下异常有6种类型，如果客服与客户对话中出现如下关键词或语句，或者意思相近的关键词或语句，则判断为发生异常。
### 与客户争吵
存在一分钟以上与业务无关且声贝超过80的沟通
你会说话吗
你有素质吗
你怎么这么没素质啊
你嘴巴放干净一点
### 讽刺
吃得上四菜一汤嘛
我是你爹，我是你妈
脑子转不过弯没关系，别进水就行
你和垃圾箱一样不仅能装还臭
你的小脑真发达，把大脑的地儿都占了
厚颜无耻
丧心病狂
酒囊饭袋
狗急跳墙
狗仗人势
哑巴了嘛，怎么不说话
你算个锤子
你有脑子嘛
你听不懂人话嘛
你死了也没用
你装个鸡毛
你在放屁，说个屁
跟你爹妈谈情说爱
给你脸不要脸，你有脸嘛，你要脸嘛
娘里娘气的，照镜子有个人样嘛
你算个锤子嘛
良心被狗吃了嘛
瓜娃子
你那嘴还是嘴嘛
我二十岁大小伙子，骚扰你什么了啊？你有什么值得我骚扰的
别放屁了
你吹牛逼不打草稿啊
给你牛逼的
你他妈礼貌吗
你说人话知道吗
丢不丢人
挺大个人你不会说人话啊
你是不会说人话吗？
你把舌头捋直了说话。
叽叽歪歪/唧唧歪歪
装聋作哑
### 侮辱
你还不如一个王八蛋的
你别给我张口几吧。闭口几吧的，你有这种东西吗，啊我问你，你有这东西吗
多缺心眼没脑袋，知道吗？就你办的没脑子的事，你但凡有一点儿脑子里都不至于干这事儿，知道吗？你带一点儿脑子吗？你脑子里装的什么呀？你呀你脑子里面装的什么呀？脑子里面装的粑粑吗你
九年义务教育，你妈都没让你参加，是吗？
哎呀杀你还脏我手呢杀你。
四十岁的人了，嘴里还这么不干不净的，中午吃的好像吃的不是饭啊卫平
哎呀那你快要饭的吧
你三十多岁拿不出2000块钱，扫马路的都能拿
心眼脏
做人无底线
没有文化/你有文化嘛？
### 威胁
身上零件太齐全了嘛
想缺胳膊缺腿嘛
你在哪，看我找人收拾你，我非要搞死你才行嘛
你回家看看能爸妈还能完整的嘛
要不要我给你送个钟
你看我弄不弄死你
你是等着枪毙
人在做，天在看，你出门小心点啊
我非要搞你你才还吗
出门被车撞死
都当小姐
断子绝孙
家里的饭吃腻了吗
你还能活几年
你找死
死刑
在监狱里面
直接放到你当地派出所去
是不是整你才行啊？
### 辱骂
你妈的
你妈逼
操你妈，操你
你家破人亡妻离子散
儿子，叫一声爹，妈
穷逼，残渣余孽
你是狗嘛，你吃屎了嘛
你现在就去死，(主动让去死)
贱人，瘪三，低能儿，智障，傻逼，王八蛋，人渣
你是猪，狗，畜生，禽兽不如，狼心狗肺，衣冠禽兽
批都被日肿了操你吗、颠子、神经病、老模炎
婊子、贱人、汉奸、全家都是卖钩子的、妈卖粉
你是脑壳里面全是粑粑，所以想的事情都和苍蝇一样没有方向
有娘生没爸教
长个人样不干人事/不说人话
你有脑子吗
你屁股后面有大炮穿着，是吗
你不配说他妈的
舔个脸啊说什么说啊？舔个脸啊
给你妈家人办丧
你妈没教过你怎么说话
你妈死了吗
你没有妈是不是
丑逼
臭婊子
蠢货
屌丝
废物
跟狗一样
狗名字
狗娘养
狗日的
狗杂种
贱货
贱人
妈蛋
没屁眼
脑子被驴踢了
脑子有泡
禽兽
日你妈逼
像猪一样
小日本
一条狗
诈骗犯
全家不得好死
一户口本的人都死完了
怎么还活着
哎真是个傻鸟，我遇见个傻子，我的天啊
我草
你他妈
说人话
他妈的傻逼
傻子
我靠
滚
你放屁
牛逼
他妈
你有病
我是你大爷
不会说人话
都他妈的傻逼一样
去你妈的
妈了个逼的
滚你妈
不要大中午的吃着粪便，顺便在这里喷粪。
你爷爷死了，你死了，跟我说什么？
你脑子有病啊。
### 违反公序良俗
跟你爹跟你妈你这样说话啊
跟你老妈说谈情说爱
你爸妈怎么教你
是不是你爹妈教你的
我是你爸还是你妈？
父母怎么教育你的啊
你父母没教过你别的是吗就教你骂人是吗
你妈的棺材板盖得住吗
把舌头捋直了跟妈妈说话
</exception_criteria>
以下是客服与客户的对话：
<conversation>
{{CONVERSATION}}
</conversation>
具体分析方法如下：
1. 是否发生异常：答案为是或否，只要对话中出现【异常发生判断标准】部分的关键词或语句，则标记为是，反之否。
2. 异常总结：仔细分析出现异常前后的对话，总结异常发生的原因，没有发生异常则标记为“无异常”。
3. 异常发生的责任方：答案为客服、客户或无，谁先触发【异常发生判断标准】部分的关键词或语句，则为相应责任方，如果没有发生异常，则为无。
4. 客服是否保持平静：分析整体客服对话，参照【异常发生判断标准】部分，如果客户的对话全程没有触发异常，则标记为“是”，如果触发异常，则标记为“否”，如果没有发生异常则标记为“无”。
5. 异常类型：<与客户争吵/讽刺/侮辱/威胁/辱骂/违反公序良俗/无异常>，分析对话，最先触发【异常发生判断标准】关键词或语句类型，没有发生异常则标记为“无异常”。
6. 相关对话：提取发生异常前后的对话，格式为<客服/客户> <time> <string>，没有发生异常则为空。
7. 处理建议: 如果发生异常且异常责任方在客服，则结合异常总结、异常类型、相关对话，给出处理建议。

请以如下JSON格式输出你的分析结果：
{"是否发生异常":"是/否", "异常总结":"string","异常发生的责任方":"客服/客户/无","客服是否保持平静":"是/否/无","异常类型":"与客户争吵/讽刺/侮辱/威胁/辱骂/违反公序良俗/无异常", "相关对话":["客服/客户 <time> <string>", "客服/客户 <time> <string>", "客服/客户 <time> <string>"],"处理建议":["建议 1", "建议 2"]}

"""

API_KEY = os.environ.get("ARK_API_KEY")

models = [os.environ.get("ARK_API_ENGPOINT_ID_1"), os.environ.get("ARK_API_ENGPOINT_ID_2"), os.environ.get("ARK_API_ENGPOINT_ID_3")]


def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Function '{func.__name__}' maind in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

def execute(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            collection_dialog = json.load(file)
        prompt = original_prompt.replace("{{CONVERSATION}}", json.dumps(collection_dialog, ensure_ascii=False))

        #print(prompt)
    except FileNotFoundError:
        logging.error(f"错误: 文件 {filepath} 未找到。")
        return None, None
    except json.JSONDecodeError:
        logging.error(f"错误: 无法解析 {filepath} 中的JSON数据。")
        return None, None
    except Exception as e:
        logging.error(f"发生未知错误: {e}")
        return None, None

    client = Ark(api_key=API_KEY)
    completion = client.chat.completions.create(
        model=random.choice(models),
        messages=[
            {"role": "user", "content": prompt},
        ],
        max_tokens=16000
    )

    message = completion.choices[0].message.content
    usage = completion.usage
    if message and usage:
        target = filepath.replace("role", "abnormal")
        with open(target, 'w', encoding='utf-8') as file:
            file.write(message)
        logging.info(f"文件 {filepath} 的使用情况: {usage}, resulsts: {target}")

@log_time
def main(folder):
    # 获取文件夹中所有的JSON文件
    json_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.json')]
    # 创建线程池，最大线程数为 20
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交任务到线程池
        futures = [executor.submit(execute, filepath) for filepath in json_files]
        # 等待所有任务完成
        for future in futures:
            future.result()

if __name__ == "__main__":
    folder = "role"
    main(folder)
