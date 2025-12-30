import matplotlib.pyplot as plt
import numpy as np

# 1. 准备核心数据
labels = ['数据要素计收', '非数据要素计收']
revenues = [1750000, 2110040]  # 去除千分位分隔符，便于计算
colors = ['#4e79a7', '#f28e2b']  # 专业配色，区分度高

# 2. 计算占比（保留1位小数）
total_revenue = sum(revenues)
percentages = [round((rev / total_revenue) * 100, 1) for rev in revenues]

# 3. 设置图表样式，解决中文乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 兼容中文显示
plt.rcParams['axes.unicode_minus'] = False  # 兼容负号显示
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)  # 高清画布

# 4. 绘制饼状图，标注金额+占比
wedges, texts, autotexts = ax.pie(
    revenues,
    labels=labels,
    colors=colors,
    autopct=lambda pct: f'¥{int(pct/100*total_revenue):,}\n({pct:.1f}%)',  # 标注金额（带千分位）+占比
    startangle=90,  # 起始角度，更美观
    textprops={'fontsize': 11}
)

# 5. 美化文本
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 6. 设置标题和图例
ax.set_title('12月份收入构成饼状图', fontsize=14, fontweight='bold', pad=20)
ax.legend(wedges, labels, loc='upper right', bbox_to_anchor=(1.2, 1))

# 7. 保存+显示图表（可注释掉plt.show()，直接保存）
plt.tight_layout()
plt.savefig('12月份收入饼状图.png', bbox_inches='tight')
plt.show()
