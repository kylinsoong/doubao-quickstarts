from transformers import BertTokenizer, BertModel
import torch
import os
import torch.nn.functional as F

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')
model = BertModel.from_pretrained('bert-base-chinese')

def bert_relevance(article: str, subject: str) -> float:
    inputs_article = tokenizer(article, return_tensors='pt', truncation=True, padding=True)
    inputs_subject = tokenizer(subject, return_tensors='pt', truncation=True, padding=True)

    with torch.no_grad():
        output_article = model(**inputs_article)
        output_subject = model(**inputs_subject)

    cls_article = output_article.last_hidden_state[:, 0, :]  # shape: (1, hidden_size)
    cls_subject = output_subject.last_hidden_state[:, 0, :]  # shape: (1, hidden_size)

    similarity = F.cosine_similarity(cls_article, cls_subject).item()

    return similarity

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
    for article in contents:
        subject = "乳腺癌"
        words = article.split()
        text = " ".join(words[:500])
        relevance_score = bert_relevance(text, subject)
        results.append(relevance_score)

    average_relevance_score = sum(results) / len(results)
    print(f"{moldel} 准确率: {average_relevance_score:.4f}")

cound("doubao-1-5-thinking", "md1")
cound("deepseek-r1", "md2")
cound("doubao-1-5-pro-32k", "md3")
