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


def cound(temperature, folder):
    contents = read_files(folder)

    results = []
    for article in contents:
        subject = "尿毒症"
        relevance_score = bert_relevance(article, subject)
        results.append(relevance_score)

    average_relevance_score = sum(results) / len(results)
    print(f"temperature: {temperature} 关联度: {average_relevance_score:.4f}")

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
