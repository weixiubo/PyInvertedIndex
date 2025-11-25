#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate query flowchart
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle
import matplotlib.font_manager as fm

# Font settings
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

def create_query_flowchart():
    """Create query processing flowchart"""
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # 标题
    ax.text(6, 13.5, 'Query Processing Flow', 
            fontsize=22, fontweight='bold', ha='center')
    ax.text(6, 13, 'Inverted Index Query Processing Flowchart', 
            fontsize=12, ha='center', style='italic', color='gray')
    
    # Color scheme
    start_color = '#27ae60'      # Green - Start/End
    process_color = '#3498db'    # Blue - Process
    decision_color = '#f39c12'   # Orange - Decision
    data_color = '#9b59b6'       # Purple - Data
    
    y = 12
    box_width = 3
    box_height = 0.6
    
    # 1. 开始
    start_box = FancyBboxPatch((6 - box_width/2, y), box_width, box_height,
                              boxstyle="round,pad=0.1",
                              edgecolor=start_color, facecolor=start_color,
                              linewidth=2, alpha=0.8)
    ax.add_patch(start_box)
    ax.text(6, y + box_height/2, 'START', fontsize=12,
            fontweight='bold', ha='center', va='center', color='white')
    
    # 箭头
    y -= 0.8
    arrow = FancyArrowPatch((6, y + 0.8), (6, y + 0.2),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2, color='black')
    ax.add_patch(arrow)
    
    # 2. 输入查询
    y -= 0.6
    input_box = FancyBboxPatch((6 - box_width/2, y), box_width, box_height,
                              boxstyle="round,pad=0.05",
                              edgecolor=process_color, facecolor=process_color,
                              linewidth=2, alpha=0.7)
    ax.add_patch(input_box)
    ax.text(6, y + box_height/2, 'Input Query', fontsize=11,
            fontweight='bold', ha='center', va='center', color='white')
    ax.text(9, y + box_height/2, 'e.g., "inverted AND index"', fontsize=9,
            ha='left', va='center', style='italic', color='gray')
    
    # 箭头
    y -= 0.8
    arrow = FancyArrowPatch((6, y + 0.8), (6, y + 0.2),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2, color='black')
    ax.add_patch(arrow)
    
    # 3. 文本预处理
    y -= 0.6
    preprocess_box = FancyBboxPatch((6 - box_width/2, y), box_width, box_height,
                                   boxstyle="round,pad=0.05",
                                   edgecolor=process_color, facecolor=process_color,
                                   linewidth=2, alpha=0.7)
    ax.add_patch(preprocess_box)
    ax.text(6, y + box_height/2, 'Text Preprocessing', fontsize=11,
            fontweight='bold', ha='center', va='center', color='white')
    
    # 预处理步骤说明
    ax.text(9.5, y + 0.4, '1. Lowercase', fontsize=8, ha='left', color='gray')
    ax.text(9.5, y + 0.1, '2. Tokenization', fontsize=8, ha='left', color='gray')
    ax.text(9.5, y - 0.2, '3. Stopword Removal', fontsize=8, ha='left', color='gray')
    
    # 箭头
    y -= 0.8
    arrow = FancyArrowPatch((6, y + 0.8), (6, y + 0.2),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2, color='black')
    ax.add_patch(arrow)
    
    # 4. 查询类型判断
    y -= 0.8
    decision_box = mpatches.FancyBboxPatch((6 - 1.2, y), 2.4, 0.8,
                                          boxstyle="round,pad=0.1",
                                          edgecolor=decision_color, facecolor=decision_color,
                                          linewidth=2, alpha=0.7)
    ax.add_patch(decision_box)
    ax.text(6, y + 0.5, 'Query Type?', fontsize=11,
            fontweight='bold', ha='center', va='center', color='white')
    ax.text(6, y + 0.15, '(Single / Boolean / Phrase)', fontsize=8,
            ha='center', va='center', color='white')
    
    # 三个分支
    y_branch = y - 0.5
    
    # 左分支：单词查询
    left_x = 2
    arrow_left = FancyArrowPatch((6 - 1.2, y + 0.4), (left_x + 1.5, y_branch + 0.8),
                                arrowstyle='->', mutation_scale=15,
                                linewidth=1.5, color='black')
    ax.add_patch(arrow_left)
    ax.text(3.5, y + 0.1, 'Single', fontsize=9, ha='center', style='italic')
    
    single_box = FancyBboxPatch((left_x, y_branch), 3, 0.6,
                               boxstyle="round,pad=0.05",
                               edgecolor='#16a085', facecolor='#16a085',
                               linewidth=1.5, alpha=0.7)
    ax.add_patch(single_box)
    ax.text(left_x + 1.5, y_branch + 0.3, 'Single Term Search', fontsize=10,
            fontweight='bold', ha='center', va='center', color='white')
    ax.text(left_x + 1.5, y_branch - 0.3, 'O(1) lookup', fontsize=8,
            ha='center', style='italic', color='gray')
    
    # 中间分支：布尔查询
    mid_x = 4.5
    arrow_mid = FancyArrowPatch((6, y), (6, y_branch + 0.6),
                               arrowstyle='->', mutation_scale=15,
                               linewidth=1.5, color='black')
    ax.add_patch(arrow_mid)
    ax.text(6.5, y - 0.2, 'Boolean', fontsize=9, ha='center', style='italic')
    
    bool_box = FancyBboxPatch((mid_x, y_branch), 3, 0.6,
                             boxstyle="round,pad=0.05",
                             edgecolor='#2980b9', facecolor='#2980b9',
                             linewidth=1.5, alpha=0.7)
    ax.add_patch(bool_box)
    ax.text(mid_x + 1.5, y_branch + 0.3, 'Boolean Query', fontsize=10,
            fontweight='bold', ha='center', va='center', color='white')
    ax.text(mid_x + 1.5, y_branch - 0.3, 'Set operations', fontsize=8,
            ha='center', style='italic', color='gray')
    
    # 右分支：短语查询
    right_x = 7
    arrow_right = FancyArrowPatch((6 + 1.2, y + 0.4), (right_x + 1.5, y_branch + 0.8),
                                 arrowstyle='->', mutation_scale=15,
                                 linewidth=1.5, color='black')
    ax.add_patch(arrow_right)
    ax.text(8.5, y + 0.1, 'Phrase', fontsize=9, ha='center', style='italic')
    
    phrase_box = FancyBboxPatch((right_x, y_branch), 3, 0.6,
                                boxstyle="round,pad=0.05",
                                edgecolor='#8e44ad', facecolor='#8e44ad',
                                linewidth=1.5, alpha=0.7)
    ax.add_patch(phrase_box)
    ax.text(right_x + 1.5, y_branch + 0.3, 'Phrase Query', fontsize=10,
            fontweight='bold', ha='center', va='center', color='white')
    ax.text(right_x + 1.5, y_branch - 0.3, 'Position validation', fontsize=8,
            ha='center', style='italic', color='gray')
    
    # 汇聚到索引查找
    y_merge = y_branch - 1.2
    
    # 三条汇聚箭头
    arrow_merge_left = FancyArrowPatch((left_x + 1.5, y_branch), (6, y_merge + 0.6),
                                      arrowstyle='->', mutation_scale=15,
                                      linewidth=1.5, color='black')
    ax.add_patch(arrow_merge_left)
    
    arrow_merge_mid = FancyArrowPatch((mid_x + 1.5, y_branch), (6, y_merge + 0.6),
                                     arrowstyle='->', mutation_scale=15,
                                     linewidth=1.5, color='black')
    ax.add_patch(arrow_merge_mid)
    
    arrow_merge_right = FancyArrowPatch((right_x + 1.5, y_branch), (6, y_merge + 0.6),
                                       arrowstyle='->', mutation_scale=15,
                                       linewidth=1.5, color='black')
    ax.add_patch(arrow_merge_right)
    
    # 5. 索引查找
    index_box = FancyBboxPatch((6 - box_width/2, y_merge), box_width, box_height,
                              boxstyle="round,pad=0.05",
                              edgecolor=data_color, facecolor=data_color,
                              linewidth=2, alpha=0.7)
    ax.add_patch(index_box)
    ax.text(6, y_merge + box_height/2, 'Index Lookup', fontsize=11,
            fontweight='bold', ha='center', va='center', color='white')
    
    # 箭头
    y = y_merge - 0.8
    arrow = FancyArrowPatch((6, y + 0.8), (6, y + 0.2),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2, color='black')
    ax.add_patch(arrow)
    
    # 6. 结果处理
    y -= 0.6
    result_box = FancyBboxPatch((6 - box_width/2, y), box_width, box_height,
                               boxstyle="round,pad=0.05",
                               edgecolor=process_color, facecolor=process_color,
                               linewidth=2, alpha=0.7)
    ax.add_patch(result_box)
    ax.text(6, y + box_height/2, 'Result Processing', fontsize=11,
            fontweight='bold', ha='center', va='center', color='white')
    
    # 箭头
    y -= 0.8
    arrow = FancyArrowPatch((6, y + 0.8), (6, y + 0.2),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2, color='black')
    ax.add_patch(arrow)
    
    # 7. 返回结果
    y -= 0.6
    output_box = FancyBboxPatch((6 - box_width/2, y), box_width, box_height,
                               boxstyle="round,pad=0.05",
                               edgecolor=process_color, facecolor=process_color,
                               linewidth=2, alpha=0.7)
    ax.add_patch(output_box)
    ax.text(6, y + box_height/2, 'Return Results', fontsize=11,
            fontweight='bold', ha='center', va='center', color='white')
    ax.text(9, y + box_height/2, 'Document IDs + Positions', fontsize=9,
            ha='left', va='center', style='italic', color='gray')
    
    # 箭头
    y -= 0.8
    arrow = FancyArrowPatch((6, y + 0.8), (6, y + 0.2),
                           arrowstyle='->', mutation_scale=20,
                           linewidth=2, color='black')
    ax.add_patch(arrow)
    
    # 8. 结束
    y -= 0.6
    end_box = FancyBboxPatch((6 - box_width/2, y), box_width, box_height,
                            boxstyle="round,pad=0.1",
                            edgecolor=start_color, facecolor=start_color,
                            linewidth=2, alpha=0.8)
    ax.add_patch(end_box)
    ax.text(6, y + box_height/2, 'END', fontsize=12,
            fontweight='bold', ha='center', va='center', color='white')
    
    # 添加图例
    legend_y = 1.5
    legend_x = 0.5
    
    # 图例框
    legend_box = FancyBboxPatch((legend_x, legend_y - 0.5), 5, 1.2,
                               boxstyle="round,pad=0.1",
                               edgecolor='#34495e', facecolor='#ecf0f1',
                               linewidth=2, alpha=0.9)
    ax.add_patch(legend_box)
    
    ax.text(legend_x + 2.5, legend_y + 0.5, 'Legend', fontsize=11,
            fontweight='bold', ha='center')
    
    # 图例项
    legend_items = [
        (start_color, 'Start/End'),
        (process_color, 'Process'),
        (decision_color, 'Decision'),
        (data_color, 'Data Access')
    ]
    
    item_y = legend_y + 0.1
    for i, (color, label) in enumerate(legend_items):
        if i == 2:
            item_y -= 0.35
            item_x = legend_x + 0.3
        else:
            item_x = legend_x + 0.3 + (i % 2) * 2.5
            if i > 0 and i % 2 == 0:
                item_y -= 0.35
        
        # 颜色块
        color_box = FancyBboxPatch((item_x, item_y), 0.3, 0.2,
                                  boxstyle="round,pad=0.02",
                                  edgecolor=color, facecolor=color,
                                  linewidth=1, alpha=0.7)
        ax.add_patch(color_box)
        ax.text(item_x + 0.5, item_y + 0.1, label, fontsize=9,
                ha='left', va='center')
    
    plt.tight_layout()

    # Save image
    output_path = '../Docs/查询流程图.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Query flowchart saved: {output_path}")
    
    return output_path

if __name__ == '__main__':
    create_query_flowchart()

