#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成倒排索引结构示意图
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import matplotlib.font_manager as fm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
plt.rcParams['axes.unicode_minus'] = False

def create_inverted_index_diagram():
    """创建倒排索引结构示意图"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Inverted Index Data Structure',
            fontsize=20, fontweight='bold', ha='center')
    ax.text(7, 9, 'Structure: {Term: {DocID: [Positions]}}',
            fontsize=14, ha='center', style='italic', color='gray')
    
    # Color scheme
    term_color = '#3498db'      # Blue - Term
    doc_color = '#2ecc71'       # Green - Document ID
    pos_color = '#e74c3c'       # Red - Position list
    bg_color = '#ecf0f1'        # Light gray - Background

    # Example: Show posting list for term "index"
    y_start = 7.5

    # Term box
    term_box = FancyBboxPatch((0.5, y_start), 2, 0.6,
                              boxstyle="round,pad=0.1",
                              edgecolor=term_color, facecolor=term_color,
                              linewidth=2, alpha=0.8)
    ax.add_patch(term_box)
    ax.text(1.5, y_start + 0.3, '"index"', fontsize=14,
            fontweight='bold', ha='center', va='center', color='white')

    # Arrow to document list
    arrow1 = FancyArrowPatch((2.5, y_start + 0.3), (3.5, y_start + 0.3),
                            arrowstyle='->', mutation_scale=20,
                            linewidth=2, color='black')
    ax.add_patch(arrow1)
    
    # Document IDs and position lists
    docs_data = [
        ('doc2', [4]),
        ('doc3', [1, 3]),
        ('doc4', [1]),
        ('doc5', [7]),
        ('doc6', [5]),
        ('doc7', [5])
    ]

    y_offset = y_start + 0.8
    for i, (doc_id, positions) in enumerate(docs_data):
        y = y_offset - i * 0.9

        # Document ID box
        doc_box = FancyBboxPatch((3.5, y - 0.3), 1.5, 0.5,
                                boxstyle="round,pad=0.05",
                                edgecolor=doc_color, facecolor=doc_color,
                                linewidth=1.5, alpha=0.7)
        ax.add_patch(doc_box)
        ax.text(4.25, y - 0.05, doc_id, fontsize=11,
                fontweight='bold', ha='center', va='center', color='white')

        # Arrow to position list
        arrow = FancyArrowPatch((5, y - 0.05), (5.8, y - 0.05),
                               arrowstyle='->', mutation_scale=15,
                               linewidth=1.5, color='black')
        ax.add_patch(arrow)

        # Position list box
        pos_text = str(positions)
        pos_width = max(1.5, len(pos_text) * 0.15)
        pos_box = FancyBboxPatch((5.8, y - 0.3), pos_width, 0.5,
                                boxstyle="round,pad=0.05",
                                edgecolor=pos_color, facecolor=pos_color,
                                linewidth=1.5, alpha=0.7)
        ax.add_patch(pos_box)
        ax.text(5.8 + pos_width/2, y - 0.05, pos_text, fontsize=10,
                ha='center', va='center', color='white', family='monospace')

        # Occurrence count annotation
        count_text = f'{len(positions)} occurrence{"s" if len(positions) > 1 else ""}'
        ax.text(5.8 + pos_width + 0.3, y - 0.05, count_text,
                fontsize=9, ha='left', va='center', color='gray', style='italic')
    
    # Statistics box
    stats_y = 1.5
    stats_box = FancyBboxPatch((0.5, stats_y - 0.5), 6.5, 1,
                              boxstyle="round,pad=0.1",
                              edgecolor='#34495e', facecolor=bg_color,
                              linewidth=2, alpha=0.9)
    ax.add_patch(stats_box)

    ax.text(1, stats_y + 0.2, 'Statistics:', fontsize=12, fontweight='bold')
    ax.text(1, stats_y - 0.1, '• Term "index" appears in 6 documents', fontsize=10)
    ax.text(1, stats_y - 0.35, '• Document Frequency (DF) = 6', fontsize=10)
    ax.text(4.5, stats_y - 0.1, '• Total occurrences = 8', fontsize=10)
    ax.text(4.5, stats_y - 0.35, '• Positions enable phrase queries', fontsize=10)
    
    # Data structure explanation
    explain_x = 8.5
    explain_y = 7.5

    # Explanation box
    explain_box = FancyBboxPatch((explain_x - 0.3, explain_y - 3.5), 5, 4,
                                boxstyle="round,pad=0.15",
                                edgecolor='#34495e', facecolor='#f8f9fa',
                                linewidth=2, alpha=0.95)
    ax.add_patch(explain_box)

    ax.text(explain_x + 2.2, explain_y + 0.2, 'Structure Explanation',
            fontsize=13, fontweight='bold', ha='center')

    # Three-layer structure explanation
    layer_y = explain_y - 0.5

    # Layer 1: Term
    term_demo = FancyBboxPatch((explain_x, layer_y), 1.2, 0.4,
                              boxstyle="round,pad=0.05",
                              edgecolor=term_color, facecolor=term_color,
                              linewidth=1.5, alpha=0.8)
    ax.add_patch(term_demo)
    ax.text(explain_x + 0.6, layer_y + 0.2, 'Term', fontsize=10,
            ha='center', va='center', color='white', fontweight='bold')
    ax.text(explain_x + 1.5, layer_y + 0.2, 'Layer 1: Term',
            fontsize=10, ha='left', va='center')

    # Layer 2: Document ID
    layer_y -= 0.8
    doc_demo = FancyBboxPatch((explain_x, layer_y), 1.2, 0.4,
                             boxstyle="round,pad=0.05",
                             edgecolor=doc_color, facecolor=doc_color,
                             linewidth=1.5, alpha=0.7)
    ax.add_patch(doc_demo)
    ax.text(explain_x + 0.6, layer_y + 0.2, 'Doc ID', fontsize=10,
            ha='center', va='center', color='white', fontweight='bold')
    ax.text(explain_x + 1.5, layer_y + 0.2, 'Layer 2: Document ID',
            fontsize=10, ha='left', va='center')

    # Layer 3: Position list
    layer_y -= 0.8
    pos_demo = FancyBboxPatch((explain_x, layer_y), 1.2, 0.4,
                             boxstyle="round,pad=0.05",
                             edgecolor=pos_color, facecolor=pos_color,
                             linewidth=1.5, alpha=0.7)
    ax.add_patch(pos_demo)
    ax.text(explain_x + 0.6, layer_y + 0.2, 'Positions', fontsize=10,
            ha='center', va='center', color='white', fontweight='bold')
    ax.text(explain_x + 1.5, layer_y + 0.2, 'Layer 3: Position List',
            fontsize=10, ha='left', va='center')

    # Advantages
    layer_y -= 1
    ax.text(explain_x + 2.2, layer_y, 'Advantages:',
            fontsize=11, fontweight='bold', ha='center')
    ax.text(explain_x + 0.2, layer_y - 0.35, '✓ O(1) term lookup', fontsize=9, color='green')
    ax.text(explain_x + 0.2, layer_y - 0.65, '✓ Boolean queries', fontsize=9, color='green')
    ax.text(explain_x + 0.2, layer_y - 0.95, '✓ Phrase queries', fontsize=9, color='green')
    ax.text(explain_x + 2.5, layer_y - 0.35, '✓ Term frequency', fontsize=9, color='green')
    ax.text(explain_x + 2.5, layer_y - 0.65, '✓ Space efficient', fontsize=9, color='green')
    ax.text(explain_x + 2.5, layer_y - 0.95, '✓ Scalable', fontsize=9, color='green')
    
    plt.tight_layout()

    # Save image
    output_path = '../Docs/倒排索引结构示意图.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Inverted index structure diagram saved: {output_path}")
    
    return output_path

if __name__ == '__main__':
    create_inverted_index_diagram()

