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


def cound(temperature, folder):
    contents = read_files(folder)

    results = []
    for i in range(0, 50):
        a = random.randint(0, 99)
        b = random.randint(0, 99)
        similarity = calculate_levenshtein_similarity(contents[a], contents[b])
        results.append(similarity)

    average_similarity = sum(results) / len(results)
    print(f"temperature: {temperature} 重复率: {average_similarity * 100:.2f}%")


cound(0.2, "mdt2")
cound(0.4, "mdt4")
cound(0.6, "mdt6")
cound(0.8, "mdt8")
cound(1.0, "mdt10")
cound(1.2, "mdt12")
cound(1.4, "mdt14")
cound(1.6, "mdt16")
cound(1.8, "mdt18")
cound(2.0, "mdt20")

