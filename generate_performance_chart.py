#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate performance comparison charts
"""

import json
import matplotlib.pyplot as plt
import numpy as np

# Font settings
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

def create_performance_charts():
    """Create comprehensive performance comparison charts"""
    
    # Load performance results
    with open('output/performance_results.json', 'r') as f:
        results = json.load(f)
    
    build_data = results['index_building']
    query_data = results['query_performance']
    
    # Create figure with 3 subplots
    fig = plt.figure(figsize=(16, 12))
    
    # Main title
    fig.suptitle('Inverted Index Performance Analysis', 
                 fontsize=20, fontweight='bold', y=0.98)
    
    # ========== Chart 1: Index Building Time vs Document Count ==========
    ax1 = plt.subplot(2, 2, 1)
    
    doc_counts = build_data['doc_counts']
    build_times = build_data['build_times']
    
    # Plot line with markers
    ax1.plot(doc_counts, build_times, 'o-', linewidth=2.5, 
             markersize=10, color='#3498db', label='Build Time')
    
    # Add value labels
    for x, y in zip(doc_counts, build_times):
        ax1.annotate(f'{y:.3f}s', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    ax1.set_xlabel('Number of Documents', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Build Time (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('Index Building Time vs Document Count', 
                  fontsize=14, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(fontsize=10)
    
    # Add performance note
    avg_time_per_doc = np.mean([t/c*1000 for t, c in zip(build_times, doc_counts)])
    ax1.text(0.98, 0.02, f'Avg: {avg_time_per_doc:.2f} ms/doc', 
             transform=ax1.transAxes, ha='right', va='bottom',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
             fontsize=9)
    
    # ========== Chart 2: Vocabulary Size Growth ==========
    ax2 = plt.subplot(2, 2, 2)
    
    vocab_sizes = build_data['vocab_sizes']
    
    ax2.plot(doc_counts, vocab_sizes, 's-', linewidth=2.5, 
             markersize=10, color='#2ecc71', label='Vocabulary Size')
    
    # Add value labels
    for x, y in zip(doc_counts, vocab_sizes):
        ax2.annotate(f'{y:,}', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=9)
    
    ax2.set_xlabel('Number of Documents', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Vocabulary Size (unique terms)', fontsize=12, fontweight='bold')
    ax2.set_title('Vocabulary Growth vs Document Count', 
                  fontsize=14, fontweight='bold', pad=15)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(fontsize=10)
    
    # ========== Chart 3: Query Performance Comparison ==========
    ax3 = plt.subplot(2, 2, 3)
    
    query_types = query_data['query_types']
    query_times = query_data['query_times']
    
    # Create bar chart
    colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
    bars = ax3.bar(range(len(query_types)), query_times, color=colors, alpha=0.8)
    
    # Add value labels on bars
    for i, (bar, time) in enumerate(zip(bars, query_times)):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{time:.3f} ms',
                ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    ax3.set_xlabel('Query Type', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Average Query Time (milliseconds)', fontsize=12, fontweight='bold')
    ax3.set_title('Query Performance by Type (1000 documents)', 
                  fontsize=14, fontweight='bold', pad=15)
    ax3.set_xticks(range(len(query_types)))
    ax3.set_xticklabels(query_types, rotation=15, ha='right')
    ax3.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    # ========== Chart 4: Performance Summary Table ==========
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')
    
    # Create summary data
    summary_data = [
        ['Metric', 'Value'],
        ['', ''],
        ['Index Building Performance', ''],
        ['Max documents tested', f'{max(doc_counts):,}'],
        ['Build time (5000 docs)', f'{build_times[-1]:.3f} seconds'],
        ['Avg time per document', f'{avg_time_per_doc:.2f} ms'],
        ['Final vocabulary size', f'{vocab_sizes[-1]:,} terms'],
        ['', ''],
        ['Query Performance (1000 docs)', ''],
        ['Single term query', f'{query_times[0]:.3f} ms'],
        ['Boolean AND query', f'{query_times[1]:.3f} ms'],
        ['Boolean OR query', f'{query_times[2]:.3f} ms'],
        ['Boolean NOT query', f'{query_times[3]:.3f} ms'],
        ['Phrase query', f'{query_times[4]:.3f} ms'],
        ['', ''],
        ['Scalability', ''],
        ['Time complexity', 'O(n) for building'],
        ['Query complexity', 'O(1) for term lookup'],
        ['Space efficiency', f'{vocab_sizes[-1]/doc_counts[-1]:.1f} terms/doc'],
    ]
    
    # Create table
    table = ax4.table(cellText=summary_data, cellLoc='left',
                     loc='center', bbox=[0, 0, 1, 1])
    
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    
    # Style the table
    for i, row in enumerate(summary_data):
        for j in range(2):
            cell = table[(i, j)]
            
            # Header row
            if i == 0:
                cell.set_facecolor('#34495e')
                cell.set_text_props(weight='bold', color='white', fontsize=11)
            # Section headers
            elif row[0] in ['Index Building Performance', 'Query Performance (1000 docs)', 'Scalability']:
                cell.set_facecolor('#3498db')
                cell.set_text_props(weight='bold', color='white')
            # Empty rows
            elif row[0] == '':
                cell.set_facecolor('#ecf0f1')
            # Data rows
            else:
                if i % 2 == 0:
                    cell.set_facecolor('#f8f9fa')
                else:
                    cell.set_facecolor('white')
            
            cell.set_edgecolor('#bdc3c7')
    
    ax4.set_title('Performance Summary', fontsize=14, fontweight='bold', pad=20)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    
    # Save figure
    output_path = '../Docs/性能对比图表.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Performance chart saved: {output_path}")
    
    return output_path

if __name__ == '__main__':
    create_performance_charts()

