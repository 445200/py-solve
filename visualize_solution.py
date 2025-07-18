#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
货物装载可视化工具

提供2D和3D视图来展示货物在货车中的装载布局
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from logistics_optimization import LogisticsOptimizer, LoadingSolution
import matplotlib.colors as mcolors

class LoadingVisualizer:
    """装载方案可视化器"""
    
    def __init__(self):
        self.colors = {
            'A': '#FF6B6B',  # 红色
            'B': '#4ECDC4',  # 青色  
            'C': '#45B7D1',  # 蓝色
            'truck': '#E8E8E8'  # 灰色
        }
    
    def visualize_2d_top_view(self, solutions):
        """2D俯视图可视化"""
        fig, axes = plt.subplots(1, len(solutions), figsize=(6*len(solutions), 6))
        if len(solutions) == 1:
            axes = [axes]
        
        for idx, solution in enumerate(solutions):
            ax = axes[idx]
            
            # 获取货车信息
            trucks = {
                'Type1': (10.0, 2.5, 2.8),
                'Type2': (12.0, 3.0, 3.0),
                'Type3': (8.0, 2.0, 2.5)
            }
            truck_dims = trucks[solution.truck_type]
            
            # 绘制货车轮廓
            truck_rect = patches.Rectangle((0, 0), truck_dims[0], truck_dims[1], 
                                         linewidth=2, edgecolor='black', 
                                         facecolor=self.colors['truck'], alpha=0.3)
            ax.add_patch(truck_rect)
            
            # 绘制货物
            for cargo in solution.cargo_instances:
                rect = patches.Rectangle((cargo.x, cargo.y), cargo.length, cargo.width,
                                       linewidth=1, edgecolor='black',
                                       facecolor=self.colors[cargo.cargo_type], alpha=0.7)
                ax.add_patch(rect)
                
                # 添加标签
                cx = cargo.x + cargo.length / 2
                cy = cargo.y + cargo.width / 2
                ax.text(cx, cy, f'{cargo.cargo_type}{cargo.instance_id}', 
                       ha='center', va='center', fontsize=8, fontweight='bold')
            
            ax.set_xlim(-0.5, truck_dims[0] + 0.5)
            ax.set_ylim(-0.5, truck_dims[1] + 0.5)
            ax.set_aspect('equal')
            ax.set_title(f'货车 {idx+1}: {solution.truck_type}\n俯视图 (长×宽)', fontsize=12)
            ax.set_xlabel('长度 (m)')
            ax.set_ylabel('宽度 (m)')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('loading_2d_top_view.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def visualize_2d_side_view(self, solutions):
        """2D侧视图可视化"""
        fig, axes = plt.subplots(1, len(solutions), figsize=(6*len(solutions), 4))
        if len(solutions) == 1:
            axes = [axes]
        
        for idx, solution in enumerate(solutions):
            ax = axes[idx]
            
            # 获取货车信息
            trucks = {
                'Type1': (10.0, 2.5, 2.8),
                'Type2': (12.0, 3.0, 3.0),
                'Type3': (8.0, 2.0, 2.5)
            }
            truck_dims = trucks[solution.truck_type]
            
            # 绘制货车轮廓
            truck_rect = patches.Rectangle((0, 0), truck_dims[0], truck_dims[2], 
                                         linewidth=2, edgecolor='black', 
                                         facecolor=self.colors['truck'], alpha=0.3)
            ax.add_patch(truck_rect)
            
            # 绘制货物
            for cargo in solution.cargo_instances:
                rect = patches.Rectangle((cargo.x, cargo.z), cargo.length, cargo.height,
                                       linewidth=1, edgecolor='black',
                                       facecolor=self.colors[cargo.cargo_type], alpha=0.7)
                ax.add_patch(rect)
                
                # 添加标签
                cx = cargo.x + cargo.length / 2
                cz = cargo.z + cargo.height / 2
                ax.text(cx, cz, f'{cargo.cargo_type}{cargo.instance_id}', 
                       ha='center', va='center', fontsize=8, fontweight='bold')
            
            ax.set_xlim(-0.5, truck_dims[0] + 0.5)
            ax.set_ylim(-0.5, truck_dims[2] + 0.5)
            ax.set_aspect('equal')
            ax.set_title(f'货车 {idx+1}: {solution.truck_type}\n侧视图 (长×高)', fontsize=12)
            ax.set_xlabel('长度 (m)')
            ax.set_ylabel('高度 (m)')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('loading_2d_side_view.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def visualize_3d(self, solution, truck_idx=0):
        """3D可视化单个货车的装载方案"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # 获取货车信息
        trucks = {
            'Type1': (10.0, 2.5, 2.8),
            'Type2': (12.0, 3.0, 3.0),
            'Type3': (8.0, 2.0, 2.5)
        }
        truck_dims = trucks[solution.truck_type]
        
        # 绘制货车框架
        self._draw_truck_frame(ax, truck_dims)
        
        # 绘制货物
        for cargo in solution.cargo_instances:
            self._draw_cargo_3d(ax, cargo)
        
        ax.set_xlim([0, truck_dims[0]])
        ax.set_ylim([0, truck_dims[1]])
        ax.set_zlim([0, truck_dims[2]])
        ax.set_xlabel('长度 (m)')
        ax.set_ylabel('宽度 (m)')
        ax.set_zlabel('高度 (m)')
        ax.set_title(f'货车 {truck_idx+1}: {solution.truck_type} - 3D装载视图')
        
        # 创建图例
        legend_elements = []
        for cargo_type in ['A', 'B', 'C']:
            legend_elements.append(patches.Patch(color=self.colors[cargo_type], 
                                               label=f'{cargo_type}类货物'))
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.savefig(f'loading_3d_truck_{truck_idx+1}.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _draw_truck_frame(self, ax, dims):
        """绘制货车框架"""
        length, width, height = dims
        
        # 定义货车的8个顶点
        vertices = [
            [0, 0, 0], [length, 0, 0], [length, width, 0], [0, width, 0],  # 底面
            [0, 0, height], [length, 0, height], [length, width, height], [0, width, height]  # 顶面
        ]
        
        # 定义货车的12条边
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # 底面边
            [4, 5], [5, 6], [6, 7], [7, 4],  # 顶面边
            [0, 4], [1, 5], [2, 6], [3, 7]   # 垂直边
        ]
        
        # 绘制边框
        for edge in edges:
            start, end = edge
            x_vals = [vertices[start][0], vertices[end][0]]
            y_vals = [vertices[start][1], vertices[end][1]]
            z_vals = [vertices[start][2], vertices[end][2]]
            ax.plot(x_vals, y_vals, z_vals, 'k-', alpha=0.3, linewidth=2)
    
    def _draw_cargo_3d(self, ax, cargo):
        """绘制3D货物"""
        x, y, z = cargo.x, cargo.y, cargo.z
        length, width, height = cargo.length, cargo.width, cargo.height
        
        # 定义立方体的8个顶点
        vertices = np.array([
            [x, y, z], [x+length, y, z], [x+length, y+width, z], [x, y+width, z],
            [x, y, z+height], [x+length, y, z+height], [x+length, y+width, z+height], [x, y+width, z+height]
        ])
        
        # 定义立方体的6个面
        faces = [
            [vertices[0], vertices[1], vertices[2], vertices[3]],  # 底面
            [vertices[4], vertices[5], vertices[6], vertices[7]],  # 顶面
            [vertices[0], vertices[1], vertices[5], vertices[4]],  # 前面
            [vertices[2], vertices[3], vertices[7], vertices[6]],  # 后面
            [vertices[1], vertices[2], vertices[6], vertices[5]],  # 右面
            [vertices[4], vertices[7], vertices[3], vertices[0]]   # 左面
        ]
        
        # 创建3D多边形集合
        poly3d = [[face] for face in faces]
        collection = Poly3DCollection(poly3d, alpha=0.7, facecolor=self.colors[cargo.cargo_type], 
                                    edgecolor='black', linewidth=0.5)
        ax.add_collection3d(collection)
        
        # 添加标签
        center_x = x + length / 2
        center_y = y + width / 2
        center_z = z + height / 2
        ax.text(center_x, center_y, center_z, f'{cargo.cargo_type}{cargo.instance_id}',
               fontsize=8, ha='center', va='center', fontweight='bold')
    
    def generate_report(self, solutions):
        """生成详细报告"""
        print("\n" + "="*80)
        print("货物装载优化详细报告")
        print("="*80)
        
        # 总体统计
        total_cost = sum(sol.total_cost for sol in solutions)
        total_weight = sum(sol.total_weight for sol in solutions)
        total_volume_used = 0
        total_volume_available = 0
        
        trucks = {
            'Type1': (10.0, 2.5, 2.8, 5000, 1000),
            'Type2': (12.0, 3.0, 3.0, 6000, 1500),
            'Type3': (8.0, 2.0, 2.5, 4000, 800)
        }
        
        for solution in solutions:
            truck_info = trucks[solution.truck_type]
            truck_volume = truck_info[0] * truck_info[1] * truck_info[2]
            total_volume_available += truck_volume
            
            cargo_volume = sum(c.length * c.width * c.height for c in solution.cargo_instances)
            total_volume_used += cargo_volume
        
        print(f"总运输费用: {total_cost} 元")
        print(f"使用货车数量: {len(solutions)} 辆")
        print(f"总载重: {total_weight} kg")
        print(f"空间利用率: {total_volume_used/total_volume_available*100:.1f}%")
        
        # 各货车详细信息
        for i, solution in enumerate(solutions, 1):
            print(f"\n--- 货车 {i}: {solution.truck_type} ---")
            truck_info = trucks[solution.truck_type]
            truck_volume = truck_info[0] * truck_info[1] * truck_info[2]
            cargo_volume = sum(c.length * c.width * c.height for c in solution.cargo_instances)
            weight_utilization = solution.total_weight / truck_info[3] * 100
            volume_utilization = cargo_volume / truck_volume * 100
            
            print(f"货车尺寸: {truck_info[0]}×{truck_info[1]}×{truck_info[2]} m")
            print(f"最大载重: {truck_info[3]} kg")
            print(f"使用费用: {solution.total_cost} 元")
            print(f"实际载重: {solution.total_weight} kg ({weight_utilization:.1f}%)")
            print(f"空间利用率: {volume_utilization:.1f}%")
            
            # 货物清单
            cargo_types = {}
            for cargo in solution.cargo_instances:
                if cargo.cargo_type not in cargo_types:
                    cargo_types[cargo.cargo_type] = []
                cargo_types[cargo.cargo_type].append(cargo)
            
            print("装载货物:")
            for cargo_type, cargos in cargo_types.items():
                print(f"  {cargo_type}类: {len(cargos)} 件")
                for cargo in cargos:
                    rotation = "旋转" if cargo.rotated else "未旋转"
                    print(f"    {cargo_type}_{cargo.instance_id}: "
                          f"({cargo.x:.1f}, {cargo.y:.1f}, {cargo.z:.1f}) "
                          f"{cargo.length:.1f}×{cargo.width:.1f}×{cargo.height:.1f} {rotation}")

def main():
    """主函数"""
    # 求解优化问题
    optimizer = LogisticsOptimizer()
    solutions = optimizer.solve()
    
    if not solutions:
        print("未找到可行解决方案！")
        return
    
    # 创建可视化器
    visualizer = LoadingVisualizer()
    
    # 生成详细报告
    visualizer.generate_report(solutions)
    
    print("\n正在生成可视化图表...")
    
    # 2D可视化
    visualizer.visualize_2d_top_view(solutions)
    visualizer.visualize_2d_side_view(solutions)
    
    # 3D可视化（每辆货车单独显示）
    for i, solution in enumerate(solutions):
        visualizer.visualize_3d(solution, i)
    
    print("所有图表已生成完成！")

if __name__ == "__main__":
    main()