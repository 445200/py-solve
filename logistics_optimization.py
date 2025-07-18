#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
物流货车调度与货物装载优化问题解决方案

该程序解决了一个3D装箱问题结合车辆调度的优化问题，
目标是在满足空间和重量约束的前提下，最小化运输总费用。
"""

import itertools
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import copy

@dataclass
class Cargo:
    """货物类"""
    name: str
    quantity: int
    length: float
    width: float
    height: float
    weight: float
    rotatable: bool
    
    def get_dimensions(self, rotated: bool = False) -> Tuple[float, float, float]:
        """获取货物尺寸，考虑旋转"""
        if rotated and self.rotatable:
            return (self.width, self.length, self.height)
        return (self.length, self.width, self.height)

@dataclass
class Truck:
    """货车类"""
    type_name: str
    length: float
    width: float
    height: float
    max_weight: float
    cost: float

@dataclass
class CargoInstance:
    """货物实例（单个货物件）"""
    cargo_type: str
    instance_id: int
    length: float
    width: float
    height: float
    weight: float
    rotatable: bool
    rotated: bool = False
    x: float = 0
    y: float = 0
    z: float = 0

@dataclass
class LoadingSolution:
    """装载方案"""
    truck_type: str
    cargo_instances: List[CargoInstance]
    total_weight: float
    total_cost: float

class LogisticsOptimizer:
    """物流优化器"""
    
    def __init__(self):
        # 初始化货物信息
        self.cargos = [
            Cargo("A", 5, 3.0, 2.0, 1.5, 800, True),
            Cargo("B", 3, 2.5, 2.0, 2.0, 1000, True),
            Cargo("C", 6, 4.0, 1.5, 1.0, 500, True)
        ]
        
        # 初始化货车信息
        self.trucks = [
            Truck("Type1", 10.0, 2.5, 2.8, 5000, 1000),
            Truck("Type2", 12.0, 3.0, 3.0, 6000, 1500),
            Truck("Type3", 8.0, 2.0, 2.5, 4000, 800)
        ]
        
        # 生成所有货物实例
        self.cargo_instances = self._generate_cargo_instances()
    
    def _generate_cargo_instances(self) -> List[CargoInstance]:
        """生成所有货物实例"""
        instances = []
        for cargo in self.cargos:
            for i in range(cargo.quantity):
                instance = CargoInstance(
                    cargo_type=cargo.name,
                    instance_id=i,
                    length=cargo.length,
                    width=cargo.width,
                    height=cargo.height,
                    weight=cargo.weight,
                    rotatable=cargo.rotatable
                )
                instances.append(instance)
        return instances
    
    def can_fit_in_truck(self, cargo_instances: List[CargoInstance], truck: Truck) -> bool:
        """检查货物是否能装入货车"""
        # 检查重量约束
        total_weight = sum(instance.weight for instance in cargo_instances)
        if total_weight > truck.max_weight:
            print(f"重量约束失败: {total_weight}kg > {truck.max_weight}kg")
            return False
        
        # 使用简化的3D装箱算法检查空间约束
        return self._check_3d_packing(cargo_instances, truck)
    
    def _check_3d_packing(self, cargo_instances: List[CargoInstance], truck: Truck) -> bool:
        """简化的3D装箱检查"""
        # 为每个货物尝试不同的旋转方式
        best_packing = self._find_best_packing(cargo_instances, truck)
        return best_packing is not None
    
    def _find_best_packing(self, cargo_instances: List[CargoInstance], truck: Truck) -> Optional[List[CargoInstance]]:
        """寻找最佳装箱方案"""
        # 首先检查重量约束
        total_weight = sum(instance.weight for instance in cargo_instances)
        if total_weight > truck.max_weight:
            return None
        
        # 使用贪心算法进行3D装箱
        packed_items = []
        occupied_spaces = []
        
        # 按体积从大到小排序
        sorted_instances = sorted(cargo_instances, 
                                key=lambda x: x.length * x.width * x.height, 
                                reverse=True)
        
        for instance in sorted_instances:
            placed = False
            
            # 尝试不旋转和旋转两种方式
            for rotated in [False, True]:
                if not instance.rotatable and rotated:
                    continue
                    
                if rotated:
                    dims = (instance.width, instance.length, instance.height)
                else:
                    dims = (instance.length, instance.width, instance.height)
                
                # 寻找可放置的位置
                position = self._find_position(dims, truck, occupied_spaces)
                if position:
                    new_instance = copy.deepcopy(instance)
                    new_instance.x, new_instance.y, new_instance.z = position
                    new_instance.rotated = rotated
                    if rotated:
                        new_instance.length, new_instance.width = new_instance.width, new_instance.length
                    
                    packed_items.append(new_instance)
                    occupied_spaces.append((position, dims))
                    placed = True
                    break
            
            if not placed:
                return None
        
        return packed_items
    
    def _find_position(self, dims: Tuple[float, float, float], 
                      truck: Truck, occupied_spaces: List) -> Optional[Tuple[float, float, float]]:
        """寻找货物的放置位置"""
        length, width, height = dims
        
        # 检查是否超出货车尺寸
        if length > truck.length or width > truck.width or height > truck.height:
            return None
        
        # 简化的位置搜索：尝试一些基本位置
        positions_to_try = [
            (0, 0, 0),  # 货车底部前左角
            (0, 0, 0),  # 其他可能的位置可以更复杂地计算
        ]
        
        for x, y, z in positions_to_try:
            # 检查是否与现有货物冲突
            if self._check_collision(x, y, z, dims, occupied_spaces):
                continue
            
            # 检查是否超出货车边界
            if (x + length <= truck.length and 
                y + width <= truck.width and 
                z + height <= truck.height):
                return (x, y, z)
        
        # 如果基本位置都不行，使用更复杂的位置搜索
        return self._advanced_position_search(dims, truck, occupied_spaces)
    
    def _advanced_position_search(self, dims: Tuple[float, float, float], 
                                 truck: Truck, occupied_spaces: List) -> Optional[Tuple[float, float, float]]:
        """高级位置搜索"""
        length, width, height = dims
        
        # 生成可能的x, y, z坐标
        x_positions = [0]
        y_positions = [0]
        z_positions = [0]
        
        # 基于已占用空间生成更多候选位置
        for (pos, space_dims) in occupied_spaces:
            x_positions.extend([pos[0] + space_dims[0], pos[0]])
            y_positions.extend([pos[1] + space_dims[1], pos[1]])
            z_positions.extend([pos[2] + space_dims[2], pos[2]])
        
        # 去重并排序
        x_positions = sorted(list(set(x_positions)))
        y_positions = sorted(list(set(y_positions)))
        z_positions = sorted(list(set(z_positions)))
        
        # 尝试所有可能的位置组合
        for x in x_positions:
            for y in y_positions:
                for z in z_positions:
                    if (x + length <= truck.length and 
                        y + width <= truck.width and 
                        z + height <= truck.height):
                        
                        if not self._check_collision(x, y, z, dims, occupied_spaces):
                            return (x, y, z)
        
        return None
    
    def _check_collision(self, x: float, y: float, z: float, 
                        dims: Tuple[float, float, float], 
                        occupied_spaces: List) -> bool:
        """检查是否与已占用空间冲突"""
        length, width, height = dims
        
        for (pos, space_dims) in occupied_spaces:
            ox, oy, oz = pos
            ol, ow, oh = space_dims
            
            # 检查3D重叠
            if (x < ox + ol and x + length > ox and
                y < oy + ow and y + width > oy and
                z < oz + oh and z + height > oz):
                return True
        
        return False
    
    def solve(self) -> List[LoadingSolution]:
        """求解优化问题"""
        print("开始求解物流货车调度与货物装载优化问题...")
        print(f"总货物数量: {len(self.cargo_instances)} 件")
        print(f"货车类型数量: {len(self.trucks)} 种")
        
        best_solutions = []
        min_cost = float('inf')
        
        # 尝试不同的车辆组合
        for max_trucks_per_type in range(1, 6):  # 限制每种类型最多使用5辆
            solutions = self._solve_with_constraint(max_trucks_per_type)
            if solutions:
                total_cost = sum(sol.total_cost for sol in solutions)
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_solutions = solutions
        
        return best_solutions
    
    def _solve_with_constraint(self, max_trucks_per_type: int) -> Optional[List[LoadingSolution]]:
        """在给定约束下求解"""
        # 使用贪心策略：优先使用性价比高的货车
        remaining_cargo = self.cargo_instances.copy()
        solutions = []
        
        # 计算每种货车的性价比（载重/成本）
        truck_efficiency = [(truck, truck.max_weight / truck.cost) for truck in self.trucks]
        truck_efficiency.sort(key=lambda x: x[1], reverse=True)
        
        while remaining_cargo:
            best_truck = None
            best_cargo_subset = None
            best_packing = None
            
            # 对每种货车类型尝试装载
            for truck, _ in truck_efficiency:
                cargo_subset, packing = self._find_best_cargo_subset(remaining_cargo, truck)
                if cargo_subset:
                    if not best_truck or len(cargo_subset) > len(best_cargo_subset):
                        best_truck = truck
                        best_cargo_subset = cargo_subset
                        best_packing = packing
            
            if not best_truck:
                return None  # 无法装载剩余货物
            
            # 创建装载方案
            total_weight = sum(item.weight for item in best_packing)
            solution = LoadingSolution(
                truck_type=best_truck.type_name,
                cargo_instances=best_packing,
                total_weight=total_weight,
                total_cost=best_truck.cost
            )
            solutions.append(solution)
            
            # 移除已装载的货物
            for item in best_cargo_subset:
                remaining_cargo.remove(item)
        
        return solutions
    
    def _find_best_cargo_subset(self, cargo_instances: List[CargoInstance], 
                               truck: Truck) -> Tuple[Optional[List[CargoInstance]], Optional[List[CargoInstance]]]:
        """为给定货车找到最佳货物子集"""
        best_subset = None
        best_packing = None
        max_items = 0
        
        # 尝试不同的货物组合
        for r in range(len(cargo_instances), 0, -1):
            for subset in itertools.combinations(cargo_instances, r):
                subset_list = list(subset)
                packing = self._find_best_packing(subset_list, truck)
                if packing and len(subset_list) > max_items:
                    max_items = len(subset_list)
                    best_subset = subset_list
                    best_packing = packing
                    
                    # 如果找到了包含很多货物的方案，就提前返回
                    if max_items >= min(r, 8):  # 限制搜索深度
                        return best_subset, best_packing
        
        return best_subset, best_packing
    
    def print_solution(self, solutions: List[LoadingSolution]):
        """打印解决方案"""
        if not solutions:
            print("未找到可行解决方案！")
            return
        
        print("\n" + "="*60)
        print("最优解决方案")
        print("="*60)
        
        total_cost = 0
        total_trucks = len(solutions)
        
        for i, solution in enumerate(solutions, 1):
            print(f"\n货车 {i}: {solution.truck_type}")
            print(f"使用费用: {solution.total_cost} 元")
            print(f"总载重: {solution.total_weight} kg")
            print("装载货物:")
            
            cargo_count = {}
            
            # 按货物类型分组显示，更清晰
            cargo_by_type = {}
            for cargo in solution.cargo_instances:
                cargo_type = cargo.cargo_type
                if cargo_type not in cargo_by_type:
                    cargo_by_type[cargo_type] = []
                cargo_by_type[cargo_type].append(cargo)
                cargo_count[cargo_type] = cargo_count.get(cargo_type, 0) + 1
            
            # 按类型显示详细装载信息
            for cargo_type in sorted(cargo_by_type.keys()):
                cargos = cargo_by_type[cargo_type]
                print(f"\n  {cargo_type}类货物 ({len(cargos)}件):")
                for cargo in sorted(cargos, key=lambda x: x.instance_id):
                    rotation_info = "(已旋转)" if cargo.rotated else "(未旋转)"
                    print(f"    {cargo_type}_{cargo.instance_id}: "
                          f"起始位置({cargo.x:.1f}, {cargo.y:.1f}, {cargo.z:.1f}) "
                          f"→ 结束位置({cargo.x + cargo.length:.1f}, {cargo.y + cargo.width:.1f}, {cargo.z + cargo.height:.1f}) "
                          f"尺寸[长×宽×高]({cargo.length:.1f}×{cargo.width:.1f}×{cargo.height:.1f}m) "
                          f"重量{cargo.weight}kg {rotation_info}")
            
            print(f"\n  货物统计:", end=" ")
            for cargo_type, count in cargo_count.items():
                print(f"{cargo_type}类{count}件", end=" ")
            print()
            
            total_cost += solution.total_cost
        
        print(f"\n总计:")
        print(f"使用货车总数: {total_trucks} 辆")
        print(f"总运输费用: {total_cost} 元")
        
        # 验证所有货物都被装载
        loaded_cargo = {}
        for solution in solutions:
            for cargo in solution.cargo_instances:
                cargo_type = cargo.cargo_type
                loaded_cargo[cargo_type] = loaded_cargo.get(cargo_type, 0) + 1
        
        print(f"\n货物装载验证:")
        all_loaded = True
        for cargo in self.cargos:
            loaded_count = loaded_cargo.get(cargo.name, 0)
            print(f"{cargo.name}类货物: 需要 {cargo.quantity} 件, 已装载 {loaded_count} 件")
            if loaded_count != cargo.quantity:
                all_loaded = False
        
        if all_loaded:
            print("✓ 所有货物都已成功装载！")
        else:
            print("✗ 部分货物未能装载！")

def main():
    """主函数"""
    optimizer = LogisticsOptimizer()
    solutions = optimizer.solve()
    optimizer.print_solution(solutions)

if __name__ == "__main__":
    main()