import os

# 总文件数
total_files = 54010

# 要统计的目录及对应显示名称
target_dirs = [
    ("asr", "asr"),
    ("input", "data clean"),
    ("role", "role assign"),
    ("loan", "tagging")
]

# 存储结果
json_counts = {}

for folder, _ in target_dirs:
    count = 0
    if os.path.isdir(folder):
        for root, _, files in os.walk(folder):
            count += sum(1 for f in files if f.endswith(".json"))
        json_counts[folder] = count
    else:
        json_counts[folder] = 0

# 构建单行输出
output_parts = []
for folder, display_name in target_dirs:
    count = json_counts[folder]
    percentage = (count / total_files) * 100 if total_files else 0
    output_parts.append(f"{display_name} finished {percentage:.2f}%")

# 拼接成指定格式（注意原示例中role assign后有两个逗号，这里按单逗号处理，如需保留双逗号可在对应位置手动添加）
print(", ".join(output_parts) + ",")
