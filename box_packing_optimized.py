#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3D装箱问题优化解决方案
计算容器内能装入的最大纸箱数量，并进行3D可视化
解决了字体显示问题，优化了视觉效果
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import math

class OptimizedBoxPacking3D:
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
        # 纸箱的6种可能摆放方向
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
        
        for i, orientation in enumerate(orientations):
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
                        'orientation_name': self._get_orientation_name(i),
                        'num_length': num_length,
                        'num_width': num_width,
                        'num_height': num_height,
                        'box_dims': (box_l, box_w, box_h)
                    }
                    
                    # 生成所有纸箱的位置
                    positions = []
                    for x_idx in range(num_length):
                        for y_idx in range(num_width):
                            for z_idx in range(num_height):
                                x = x_idx * box_l
                                y = y_idx * box_w
                                z = z_idx * box_h
                                positions.append((x, y, z, box_l, box_w, box_h))
                    best_positions = positions
        
        self.max_boxes = max_boxes
        self.best_config = best_config
        self.box_positions = best_positions
        
        return max_boxes, best_config
    
    def _get_orientation_name(self, orientation_index):
        """获取摆放方向的名称"""
        names = [
            "Original Orientation",
            "Rotated 90°", 
            "Side Placement 1",
            "Side Placement 2", 
            "Vertical Placement 1",
            "Vertical Placement 2"
        ]
        return names[orientation_index]
    
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
    
    def create_3d_visualization(self, show_sample_only=False):
        """
        创建3D装箱图
        
        Args:
            show_sample_only: 如果为True，只显示部分纸箱（用于大量纸箱的情况）
        """
        fig = plt.figure(figsize=(16, 12))
        ax = fig.add_subplot(111, projection='3d')
        
        # 绘制容器边框
        self._draw_container_frame(ax)
        
        # 决定显示哪些纸箱
        positions_to_draw = self.box_positions
        if show_sample_only and len(self.box_positions) > 100:
            # 如果纸箱太多，只显示一部分
            step = max(1, len(self.box_positions) // 50)
            positions_to_draw = self.box_positions[::step]
            
        # 绘制纸箱
        self._draw_boxes(ax, positions_to_draw)
        
        # 设置图形属性 (使用英文避免字体问题)
        ax.set_xlabel('Length (mm)', fontsize=12)
        ax.set_ylabel('Width (mm)', fontsize=12)
        ax.set_zlabel('Height (mm)', fontsize=12)
        ax.set_title('3D Box Packing Visualization', fontsize=16, fontweight='bold')
        
        # 设置坐标轴范围
        ax.set_xlim(0, self.container_length)
        ax.set_ylim(0, self.container_width)
        ax.set_zlim(0, self.container_height)
        
        # 设置视角
        ax.view_init(elev=20, azim=45)
        
        # 添加网格
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return fig
    
    def _draw_container_frame(self, ax):
        """绘制容器边框"""
        # 容器的8个顶点
        vertices = np.array([
            [0, 0, 0],
            [self.container_length, 0, 0],
            [self.container_length, self.container_width, 0],
            [0, self.container_width, 0],
            [0, 0, self.container_height],
            [self.container_length, 0, self.container_height],
            [self.container_length, self.container_width, self.container_height],
            [0, self.container_width, self.container_height]
        ])
        
        # 容器的边
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # 底面
            [4, 5], [5, 6], [6, 7], [7, 4],  # 顶面
            [0, 4], [1, 5], [2, 6], [3, 7]   # 竖直边
        ]
        
        for edge in edges:
            points = vertices[[edge[0], edge[1]]]
            ax.plot3D(points[:, 0], points[:, 1], points[:, 2], 
                     'k-', linewidth=3, alpha=0.8)
    
    def _draw_boxes(self, ax, positions_to_draw):
        """绘制纸箱"""
        # 使用更好的颜色映射
        colors = plt.cm.tab20(np.linspace(0, 1, min(20, len(positions_to_draw))))
        
        for i, (x, y, z, l, w, h) in enumerate(positions_to_draw):
            color = colors[i % len(colors)]
            
            # 创建纸箱的6个面
            faces = []
            
            # 底面和顶面
            faces.append([[x, x+l, x+l, x], [y, y, y+w, y+w], [z, z, z, z]])
            faces.append([[x, x+l, x+l, x], [y, y, y+w, y+w], [z+h, z+h, z+h, z+h]])
            
            # 前面和后面
            faces.append([[x, x+l, x+l, x], [y, y, y, y], [z, z, z+h, z+h]])
            faces.append([[x, x+l, x+l, x], [y+w, y+w, y+w, y+w], [z, z, z+h, z+h]])
            
            # 左面和右面
            faces.append([[x, x, x, x], [y, y+w, y+w, y], [z, z, z+h, z+h]])
            faces.append([[x+l, x+l, x+l, x+l], [y, y+w, y+w, y], [z, z, z+h, z+h]])
            
            for face in faces:
                vertices = list(zip(face[0], face[1], face[2]))
                poly = [vertices]
                ax.add_collection3d(Poly3DCollection(poly, alpha=0.4, 
                                                   facecolor=color,
                                                   edgecolor='black', linewidth=0.5))
    
    def print_detailed_results(self):
        """打印详细计算结果"""
        results = self.calculate_remaining_space()
        
        print("=" * 80)
        print("3D BOX PACKING CALCULATION RESULTS")
        print("=" * 80)
        print(f"Container Dimensions: {self.container_length} × {self.container_width} × {self.container_height} mm")
        print(f"Box Dimensions: {self.box_length} × {self.box_width} × {self.box_height} mm")
        print()
        
        if self.best_config:
            config = self.best_config
            print(f"OPTIMAL PACKING SOLUTION:")
            print(f"  Box Placement Orientation: {config['orientation_name']}")
            print(f"  Box Actual Dimensions: {config['box_dims'][0]} × {config['box_dims'][1]} × {config['box_dims'][2]} mm")
            print(f"  Boxes in Length Direction: {config['num_length']} pieces")
            print(f"  Boxes in Width Direction: {config['num_width']} pieces")
            print(f"  Boxes in Height Direction: {config['num_height']} pieces")
            print(f"  TOTAL BOX COUNT: {self.max_boxes} pieces")
            print()
            
            print(f"REMAINING SPACE:")
            print(f"  Remaining Length: {results['remaining_length']:.1f} mm")
            print(f"  Remaining Width: {results['remaining_width']:.1f} mm")
            print(f"  Remaining Height: {results['remaining_height']:.1f} mm")
            print()
            
            print(f"VOLUME CALCULATIONS:")
            print(f"  Container Total Volume: {results['container_volume']/1e9:.3f} m³")
            print(f"  Single Box Volume: {results['single_box_volume']/1e9:.6f} m³")
            print(f"  Total Cargo Volume: {results['total_boxes_volume']/1e9:.3f} m³")
            print(f"  VOLUME UTILIZATION RATE: {results['volume_utilization']:.2f}%")
            print()
            
            # 计算重量相关信息（假设纸箱重量）
            box_weight_kg = 2.0  # 假设每个纸箱重2kg
            total_weight = self.max_boxes * box_weight_kg
            print(f"WEIGHT ESTIMATION (assuming {box_weight_kg}kg per box):")
            print(f"  Total Weight: {total_weight:.1f} kg ({total_weight/1000:.2f} tons)")
            
        else:
            print("ERROR: Cannot fit any boxes in the container!")
        
        print("=" * 80)
    
    def export_results_to_file(self, filename="packing_results.txt"):
        """将结果导出到文件"""
        results = self.calculate_remaining_space()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("3D BOX PACKING CALCULATION RESULTS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Container Dimensions: {self.container_length} × {self.container_width} × {self.container_height} mm\n")
            f.write(f"Box Dimensions: {self.box_length} × {self.box_width} × {self.box_height} mm\n\n")
            
            if self.best_config:
                config = self.best_config
                f.write("OPTIMAL PACKING SOLUTION:\n")
                f.write(f"  Box Placement Orientation: {config['orientation_name']}\n")
                f.write(f"  Box Actual Dimensions: {config['box_dims'][0]} × {config['box_dims'][1]} × {config['box_dims'][2]} mm\n")
                f.write(f"  Boxes in Length Direction: {config['num_length']} pieces\n")
                f.write(f"  Boxes in Width Direction: {config['num_width']} pieces\n")
                f.write(f"  Boxes in Height Direction: {config['num_height']} pieces\n")
                f.write(f"  TOTAL BOX COUNT: {self.max_boxes} pieces\n\n")
                
                f.write("REMAINING SPACE:\n")
                f.write(f"  Remaining Length: {results['remaining_length']:.1f} mm\n")
                f.write(f"  Remaining Width: {results['remaining_width']:.1f} mm\n")
                f.write(f"  Remaining Height: {results['remaining_height']:.1f} mm\n\n")
                
                f.write("VOLUME CALCULATIONS:\n")
                f.write(f"  Container Total Volume: {results['container_volume']/1e9:.3f} m³\n")
                f.write(f"  Single Box Volume: {results['single_box_volume']/1e9:.6f} m³\n")
                f.write(f"  Total Cargo Volume: {results['total_boxes_volume']/1e9:.3f} m³\n")
                f.write(f"  VOLUME UTILIZATION RATE: {results['volume_utilization']:.2f}%\n")
        
        print(f"Results exported to: {filename}")

def main():
    """主函数"""
    # 定义尺寸 (mm)
    container_dims = (13500, 2440, 2680)  # 容器尺寸
    box_dims = (680, 680, 235)            # 纸箱尺寸
    
    print("Starting 3D Box Packing Analysis...")
    print(f"Container: {container_dims[0]} × {container_dims[1]} × {container_dims[2]} mm")
    print(f"Box: {box_dims[0]} × {box_dims[1]} × {box_dims[2]} mm")
    print("-" * 50)
    
    # 创建装箱计算器
    packing = OptimizedBoxPacking3D(container_dims, box_dims)
    
    # 计算最优装箱方案
    max_boxes, best_config = packing.calculate_max_boxes()
    
    # 打印详细结果
    packing.print_detailed_results()
    
    # 导出结果到文件
    packing.export_results_to_file()
    
    # 创建3D可视化
    if max_boxes > 0:
        print("Generating 3D visualization...")
        
        # 如果纸箱数量太多，只显示部分
        show_sample = max_boxes > 100
        if show_sample:
            print(f"Too many boxes ({max_boxes}), showing sample visualization...")
            
        fig = packing.create_3d_visualization(show_sample_only=show_sample)
        
        # 保存图片
        output_filename = 'optimized_3d_box_packing.png'
        plt.savefig(output_filename, dpi=300, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        print(f"3D visualization saved as: {output_filename}")
        
        # 尝试显示图形（在交互环境中）
        try:
            plt.show()
        except:
            print("Note: Interactive display not available in this environment.")
    
    return packing

if __name__ == "__main__":
    # 设置matplotlib参数
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    
    # 运行主程序
    packing_result = main()