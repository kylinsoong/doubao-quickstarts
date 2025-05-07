import os
import numpy as np
from typing import List
from volcenginesdkarkruntime._exceptions import ArkAPIError
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")

client = Ark(api_key=API_KEY)


def test_embeddings(endpoint_id, inputs):
    print("----- embeddings request -----")
    try:
        resp = client.embeddings.create(
            model=endpoint_id,
            input=inputs
        )
        return resp
    except ArkAPIError as e:
        print(e)

def sliced_norm_l2(vec: List[float], dim=2048) -> List[float]:
    # dim 取值 512,1024,2048
    norm = float(np.linalg.norm(vec[ :dim]))
    return [v / norm for v in vec[ :dim]]

if __name__ == '__main__':
    # 检索 query 建议添加 instruction 前缀
    query_instruction = '为这个句子生成表示以用于检索相关文章：'
    query = "天是什么颜色？"
    # 向量索引的 document 则不添加 instruction
    document = "天空呈现颜色主要与“瑞利散射”现象有关，具体形成过程如下：太阳光是由红、橙、黄、绿、蓝、靛、紫等多种颜色的光混合而成的。大气中存在着无数的气体分子和其他微粒。当太阳光进入地球大气层时，波长较长的红光、橙光、黄光能穿透大气层，直接射到地面，而波长较短的蓝、紫、靛等色光，很容易被悬浮在空气中的微粒阻挡，从而使光线散射向四方。其中蓝光波长较短，散射作用更强，因此我们眼睛看到的天空主要呈现蓝色。在一些特殊情况下，如傍晚或早晨，阳光斜射角度大，通过大气层的路径较长，蓝光等短波长光被散射得更多，而红光等长波长光散射损失较少，这时天空可能会呈现橙红色等其他颜色。"
    
    inputs = [
        query_instruction + query, # query text
        document, # document text
    ]

    resp = test_embeddings(endpoint_id="ep-20250430143556-jd5sf", inputs=inputs) # endpoint 使用方舟 2.0 模型接入


    print(resp)
