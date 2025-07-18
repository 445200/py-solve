#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D装箱问题解决方案
计算容器内能装入的最大纸箱数量，并进行3D可视化
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import math

class BoxPacking3D:
    def __init__(self, container_dims, box_dims):
        """
        初始化装箱计算器
        
        Args:
            container_dims: 容器尺寸 (长, 宽, 高) mm
            box_dims: 纸箱尺寸 (长, 宽, 高) mm
        """
        self.container_length, self.container_width, self.container_height = container_dims
        self.box_length, self.box_width, self.box_height = box_dims
        self.box_positions = []
        
    def calculate_max_boxes(self):
        """
        计算最多能装入的纸箱数量
        考虑所有可能的旋转方向
        """
        # 纸箱的三种可能摆放方向
        orientations = [
            (self.box_length, self.box_width, self.box_height),    # 原始方向
            (self.box_width, self.box_length, self.box_height),    # 旋转90度
            (self.box_length, self.box_height, self.box_width),    # 侧放1
            (self.box_width, self.box_height, self.box_length),    # 侧放2
            (self.box_height, self.box_length, self.box_width),    # 立放1
            (self.box_height, self.box_width, self.box_length)     # 立放2
        ]
        
        max_boxes = 0
        best_config = None
        best_positions = []
        
        for orientation in orientations:
            box_l, box_w, box_h = orientation
            
            # 检查是否能放入容器
            if (box_l <= self.container_length and 
                box_w <= self.container_width and 
                box_h <= self.container_height):
                
                # 计算每个方向能放多少个
                num_length = int(self.container_length // box_l)
                num_width = int(self.container_width // box_w)
                num_height = int(self.container_height // box_h)
                
                total_boxes = num_length * num_width * num_height
                
                if total_boxes > max_boxes:
                    max_boxes = total_boxes
                    best_config = {
                        'orientation': orientation,
                        'num_length': num_length,
                        'num_width': num_width,
                        'num_height': num_height,
                        'box_dims': (box_l, box_w, box_h)
                    }
                    
                    # 生成所有纸箱的位置
                    positions = []
                    for i in range(num_length):
                        for j in range(num_width):
                            for k in range(num_height):
                                x = i * box_l
                                y = j * box_w
                                z = k * box_h
                                positions.append((x, y, z, box_l, box_w, box_h))
                    best_positions = positions
        
        self.max_boxes = max_boxes
        self.best_config = best_config
        self.box_positions = best_positions
        
        return max_boxes, best_config
    
    def calculate_remaining_space(self):
        """
        计算剩余空间和利用率
        """
        if not self.best_config:
            return None
            
        config = self.best_config
        box_l, box_w, box_h = config['box_dims']
        
        # 计算剩余尺寸
        remaining_length = self.container_length - (config['num_length'] * box_l)
        remaining_width = self.container_width - (config['num_width'] * box_w)
        remaining_height = self.container_height - (config['num_height'] * box_h)
        
        # 计算体积
        container_volume = self.container_length * self.container_width * self.container_height
        single_box_volume = self.box_length * self.box_width * self.box_height
        total_boxes_volume = self.max_boxes * single_box_volume
        
        # 体积利用率
        volume_utilization = (total_boxes_volume / container_volume) * 100
        
        return {
            'remaining_length': remaining_length,
            'remaining_width': remaining_width,
            'remaining_height': remaining_height,
            'container_volume': container_volume,
            'single_box_volume': single_box_volume,
            'total_boxes_volume': total_boxes_volume,
            'volume_utilization': volume_utilization,
            'box_count': self.max_boxes
        }
    
    def create_3d_visualization(self):
        """
        创建3D装箱图
        """
        fig = plt.figure(figsize=(15, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制容器边框
        self._draw_container_frame(ax)
        
        # 绘制纸箱
        self._draw_boxes(ax)
        
        # 设置图形属性
        ax.set_xlabel('长度 (mm)', fontsize=12)
        ax.set_ylabel('宽度 (mm)', fontsize=12)
        ax.set_zlabel('高度 (mm)', fontsize=12)
        ax.set_title('3D装箱图', fontsize=16, fontweight='bold')
        
        # 设置坐标轴范围
        ax.set_xlim(0, self.container_length)
        ax.set_ylim(0, self.container_width)
        ax.set_zlim(0, self.container_height)
        
        # 设置视角
        ax.view_init(elev=20, azim=45)
        
        plt.tight_layout()
        return fig
    
    def _draw_container_frame(self, ax):
        """绘制容器边框"""
        # 容器的8个顶点
        vertices = [
            [0, 0, 0],
            [self.container_length, 0, 0],
            [self.container_length, self.container_width, 0],
            [0, self.container_width, 0],
            [0, 0, self.container_height],
            [self.container_length, 0, self.container_height],
            [self.container_length, self.container_width, self.container_height],
            [0, self.container_width, self.container_height]
        ]
        
        # 容器的边
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # 底面
            [4, 5], [5, 6], [6, 7], [7, 4],  # 顶面
            [0, 4], [1, 5], [2, 6], [3, 7]   # 竖直边
        ]
        
        for edge in edges:
            points = np.array([vertices[edge[0]], vertices[edge[1]]])
            ax.plot3D(points[:, 0], points[:, 1], points[:, 2], 'k-', linewidth=2, alpha=0.8)
    
    def _draw_boxes(self, ax):
        """绘制纸箱"""
        colors = plt.cm.Set3(np.linspace(0, 1, len(self.box_positions)))
        
        for i, (x, y, z, l, w, h) in enumerate(self.box_positions):
            # 创建纸箱的6个面
            faces = [
                # 底面和顶面
                [[x, x+l, x+l, x], [y, y, y+w, y+w], [z, z, z, z]],
                [[x, x+l, x+l, x], [y, y, y+w, y+w], [z+h, z+h, z+h, z+h]],
                # 前面和后面
                [[x, x+l, x+l, x], [y, y, y, y], [z, z, z+h, z+h]],
                [[x, x+l, x+l, x], [y+w, y+w, y+w, y+w], [z, z, z+h, z+h]],
                # 左面和右面
                [[x, x, x, x], [y, y+w, y+w, y], [z, z, z+h, z+h]],
                [[x+l, x+l, x+l, x+l], [y, y+w, y+w, y], [z, z, z+h, z+h]]
            ]
            
            for face in faces:
                vertices = list(zip(face[0], face[1], face[2]))
                poly = [[vertices[0], vertices[1], vertices[2], vertices[3]]]
                ax.add_collection3d(Poly3DCollection(poly, alpha=0.3, 
                                                   facecolor=colors[i % len(colors)],
                                                   edgecolor='black', linewidth=0.5))
    
    def print_results(self):
        """打印计算结果"""
        results = self.calculate_remaining_space()
        
        print("=" * 60)
        print("3D装箱计算结果")
        print("=" * 60)
        print(f"容器尺寸: {self.container_length} × {self.container_width} × {self.container_height} mm")
        print(f"纸箱尺寸: {self.box_length} × {self.box_width} × {self.box_height} mm")
        print()
        
        if self.best_config:
            config = self.best_config
            print(f"最优装箱方案:")
            print(f"  纸箱摆放尺寸: {config['box_dims'][0]} × {config['box_dims'][1]} × {config['box_dims'][2]} mm")
            print(f"  长度方向数量: {config['num_length']} 个")
            print(f"  宽度方向数量: {config['num_width']} 个")
            print(f"  高度方向数量: {config['num_height']} 个")
            print(f"  总装箱数量: {self.max_boxes} 个")
            print()
            
            print(f"空间计算:")
            print(f"  长度剩余: {results['remaining_length']:.1f} mm")
            print(f"  宽度剩余: {results['remaining_width']:.1f} mm")
            print(f"  高度剩余: {results['remaining_height']:.1f} mm")
            print()
            
            print(f"体积计算:")
            print(f"  容器总体积: {results['container_volume']/1e9:.3f} m³")
            print(f"  单个纸箱体积: {results['single_box_volume']/1e9:.6f} m³")
            print(f"  货物总体积: {results['total_boxes_volume']/1e9:.3f} m³")
            print(f"  体积利用率: {results['volume_utilization']:.2f}%")
        else:
            print("无法装入任何纸箱！")
        
        print("=" * 60)

def main():
    """主函数"""
    # 定义尺寸 (mm)
    container_dims = (13500, 2440, 2680)  # 容器尺寸
    box_dims = (680, 680, 235)            # 纸箱尺寸
    
    # 创建装箱计算器
    packing = BoxPacking3D(container_dims, box_dims)
    
    # 计算最优装箱方案
    max_boxes, best_config = packing.calculate_max_boxes()
    
    # 打印结果
    packing.print_results()
    
    # 创建3D可视化
    if max_boxes > 0:
        fig = packing.create_3d_visualization()
        
        # 保存图片
        plt.savefig('3d_box_packing.png', dpi=300, bbox_inches='tight')
        print(f"3D装箱图已保存为: 3d_box_packing.png")
        
        # 显示图形
        plt.show()
    
    return packing

if __name__ == "__main__":
    # 设置中文字体支持
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    # 运行主程序
    packing_result = main()