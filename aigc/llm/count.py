import os
import hashlib
from collections import defaultdict

def hash_file(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

folder = 'md1'  
hash_map = defaultdict(list)

# 遍历所有 .md 文件
for file in os.listdir(folder):
    if file.endswith('.md'):
        file_path = os.path.join(folder, file)
        file_hash = hash_file(file_path)
        hash_map[file_hash].append(file)

# 输出重复文件组
total_files = 0
duplicate_groups = 0
for files in hash_map.values():
    total_files += len(files)
    if len(files) > 1:
        duplicate_groups += 1
        print(f"🔁 Duplicate group ({len(files)} files): {files}")

print(f"\n📊 Total files: {total_files}")
print(f"♻️  Duplicate groups: {duplicate_groups}")
print(f"📈  Duplicate rate: {round((total_files - len(hash_map)) / total_files * 100, 2)}%")

