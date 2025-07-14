from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patheffects as PathEffects

# 手动指定字体文件路径
font_path = '/System/Library/Fonts/STHeiti Medium.ttc'
font = FontProperties(fname=font_path)

# 创建图形和轴
fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

# 定义阶段和时间
phases = ['第一阶段\n(1-2年)', '第二阶段\n(2-3年)', '第三阶段\n(4-5年)']
phase_titles = ['基础智能体建设', '进阶智能体建设', '高级智能体建设']
phase_contents = [
    '• 智能体平台基础建设\n• 通用型智能体开发\n• 部门专项智能体(优先级高)',
    '• 智能体平台能力扩展\n• 专业分析型智能体开发\n• 部门专项智能体(中等复杂度)',
    '• 智能体平台高级能力建设\n• 决策支持型智能体开发\n• 部门专项智能体(高复杂度)'
]

# 设置颜色
colors = ['#4472C4', '#70AD47', '#ED7D31']
text_colors = ['white', 'white', 'white']

# 绘制时间轴
ax.plot([0, 5], [0, 0], 'k-', linewidth=2)
for i in range(6):
    ax.plot([i, i], [-0.1, 0.1], 'k-', linewidth=2)
    ax.text(i, -0.4, f'{i}年', ha='center', fontsize=12, fontproperties=font)

# 绘制阶段块
heights = [1.5, 1.5, 1.5]
y_positions = [0.5, 0.5, 0.5]
widths = [2, 2, 2]
start_positions = [0, 2, 3]

for i, (phase, title, content) in enumerate(zip(phases, phase_titles, phase_contents)):
    # 绘制阶段块
    rect = Rectangle((start_positions[i], y_positions[i] - heights[i]/2), 
                    widths[i], heights[i], 
                    facecolor=colors[i], alpha=0.8, edgecolor='black')
    ax.add_patch(rect)
    
    # 添加阶段名称
    ax.text(start_positions[i] + widths[i]/2, y_positions[i] + heights[i]/2 - 0.2, 
            phase, ha='center', va='center', color=text_colors[i], fontsize=14, fontweight='bold', fontproperties=font)
    
    # 添加阶段标题
    ax.text(start_positions[i] + widths[i]/2, y_positions[i] + 0.2, 
            title, ha='center', va='center', color=text_colors[i], fontsize=16, fontweight='bold', fontproperties=font)
    
    # 添加阶段内容
    ax.text(start_positions[i] + widths[i]/2, y_positions[i] - 0.3, 
            content, ha='center', va='center', color=text_colors[i], fontsize=10, fontproperties=font)

# 设置轴范围和隐藏轴
ax.set_xlim(-0.5, 5.5)
ax.set_ylim(-0.5, 2.5)
ax.axis('off')

# 添加标题
ax.text(2.5, 2.3, '中心财务5年智能体建设规划路线图', ha='center', fontsize=18, fontweight='bold', fontproperties=font)

# 添加注释
ax.text(5.3, -0.4, '注：时间轴表示从项目启动开始计算的年数', fontsize=10, ha='right', fontproperties=font)

# 保存图表
plt.tight_layout()
plt.savefig('output/roadmap_chart.png', dpi=300, bbox_inches='tight')
plt.close()
