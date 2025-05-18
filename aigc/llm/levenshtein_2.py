import Levenshtein  # 需额外安装：pip install python-Levenshtein
import os
import random

def calculate_levenshtein_similarity(text1, text2):
    """计算两篇文本的编辑距离相似度"""
    distance = Levenshtein.distance(text1, text2)
    max_length = max(len(text1), len(text2))
    if max_length == 0:
        return 1.0
    return 1.0 - (distance / max_length)

def read_files(folder):
    file_contents = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_contents.append(content)
    return file_contents


def cound(moldel, folder):
    contents = read_files(folder)

    results = []
    for i in range(0, 100):
        a = random.randint(0, 199)
        b = random.randint(0, 199)
        similarity = calculate_levenshtein_similarity(contents[a], contents[b])
        results.append(similarity)

    average_similarity = sum(results) / len(results)
    print(f"{moldel} 重复率: {average_similarity * 100:.2f}%")


cound("doubao-1-5-thinking", "md4")
cound("deepseek-r1", "md5")
cound("doubao-1-5-pro-32k", "md6")



