import re
import os

def count_words(text):
    chinese_chars = re.findall(r'[\u4e00-\u9fa5]', text)
    return len(chinese_chars)


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

def cound(folder):
    contents = read_files(folder)

    results = []
    for article in contents:
        results.append(count_words(article))

    average_length = int(sum(results) / len(results))

    print(f"{folder} 文章字数: {average_length}")

cound("md1")
cound("md2")
cound("md3")
cound("md4")
cound("md5")
cound("md6")
cound("md7")
cound("md8")
cound("md9")
