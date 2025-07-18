#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的装箱布局可视化
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def create_layout_diagram():
    """创建装箱布局示意图"""
    
    # 容器和纸箱尺寸 (mm)
    container_dims = (13500, 2440, 2680)
    box_dims = (680, 680, 235)
    
    # 计算布局
    num_length = 19  # 长度方向
    num_width = 3    # 宽度方向  
    num_height = 11  # 高度方向
    
    # 创建图形
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. 顶视图 (从上往下看)
    ax1.set_xlim(0, container_dims[0])
    ax1.set_ylim(0, container_dims[1])
    
    for i in range(num_length):
        for j in range(num_width):
            x = i * box_dims[0]
            y = j * box_dims[1]
            rect = patches.Rectangle((x, y), box_dims[0], box_dims[1], 
                                   linewidth=1, edgecolor='blue', facecolor='lightblue', alpha=0.7)
            ax1.add_patch(rect)
    
    ax1.set_title('Top View (Looking Down)\nContainer: 13500×2440 mm', fontsize=12)
    ax1.set_xlabel('Length (mm)')
    ax1.set_ylabel('Width (mm)')
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')
    
    # 2. 侧视图 (从侧面看)
    ax2.set_xlim(0, container_dims[0])
    ax2.set_ylim(0, container_dims[2])
    
    for i in range(num_length):
        for k in range(num_height):
            x = i * box_dims[0]
            z = k * box_dims[2]
            rect = patches.Rectangle((x, z), box_dims[0], box_dims[2], 
                                   linewidth=1, edgecolor='red', facecolor='lightcoral', alpha=0.7)
            ax2.add_patch(rect)
    
    ax2.set_title('Side View (Length×Height)\nContainer: 13500×2680 mm', fontsize=12)
    ax2.set_xlabel('Length (mm)')
    ax2.set_ylabel('Height (mm)')
    ax2.grid(True, alpha=0.3)
    ax2.set_aspect('equal')
    
    # 3. 前视图 (从前面看)
    ax3.set_xlim(0, container_dims[1])
    ax3.set_ylim(0, container_dims[2])
    
    for j in range(num_width):
        for k in range(num_height):
            y = j * box_dims[1]
            z = k * box_dims[2]
            rect = patches.Rectangle((y, z), box_dims[1], box_dims[2], 
                                   linewidth=1, edgecolor='green', facecolor='lightgreen', alpha=0.7)
            ax3.add_patch(rect)
    
    ax3.set_title('Front View (Width×Height)\nContainer: 2440×2680 mm', fontsize=12)
    ax3.set_xlabel('Width (mm)')
    ax3.set_ylabel('Height (mm)')
    ax3.grid(True, alpha=0.3)
    ax3.set_aspect('equal')
    
    # 4. 统计信息
    ax4.axis('off')
    
    # 计算结果
    total_boxes = num_length * num_width * num_height
    remaining_length = container_dims[0] - (num_length * box_dims[0])
    remaining_width = container_dims[1] - (num_width * box_dims[1])
    remaining_height = container_dims[2] - (num_height * box_dims[2])
    
    container_volume = container_dims[0] * container_dims[1] * container_dims[2]
    box_volume = box_dims[0] * box_dims[1] * box_dims[2]
    total_cargo_volume = total_boxes * box_volume
    utilization = (total_cargo_volume / container_volume) * 100
    
    info_text = f"""
PACKING CALCULATION RESULTS
===========================

Container Dimensions:
  Length: {container_dims[0]:,} mm
  Width: {container_dims[1]:,} mm  
  Height: {container_dims[2]:,} mm

Box Dimensions:
  Length: {box_dims[0]} mm
  Width: {box_dims[1]} mm
  Height: {box_dims[2]} mm

LAYOUT ARRANGEMENT:
  Length direction: {num_length} boxes
  Width direction: {num_width} boxes
  Height direction: {num_height} boxes
  
TOTAL BOX COUNT: {total_boxes} pieces

REMAINING SPACE:
  Length: {remaining_length} mm
  Width: {remaining_width} mm
  Height: {remaining_height} mm

VOLUME EFFICIENCY:
  Container Volume: {container_volume/1e9:.3f} m³
  Cargo Volume: {total_cargo_volume/1e9:.3f} m³
  Utilization Rate: {utilization:.2f}%

WEIGHT ESTIMATE:
  Total Weight: {total_boxes * 2:.0f} kg (2kg/box)
    """
    
    ax4.text(0.05, 0.95, info_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('layout_diagram.png', dpi=300, bbox_inches='tight')
    print("Layout diagram saved as: layout_diagram.png")
    
    return fig

if __name__ == "__main__":
    create_layout_diagram()
    plt.show()