#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化版物流优化分析工具
不依赖外部库，生成文本格式的详细分析报告
"""

from logistics_optimization import LogisticsOptimizer

def generate_ascii_layout(solution, truck_idx):
    """生成ASCII格式的货车装载布局图"""
    # 获取货车信息
    trucks = {
        'Type1': (10.0, 2.5, 2.8),
        'Type2': (12.0, 3.0, 3.0),
        'Type3': (8.0, 2.0, 2.5)
    }
    truck_dims = trucks[solution.truck_type]
    
    print(f"\n=== 货车 {truck_idx} ({solution.truck_type}) 装载布局图 ===")
    print(f"货车尺寸: {truck_dims[0]}m × {truck_dims[1]}m × {truck_dims[2]}m")
    print("俯视图 (长×宽):")
    
    # 创建简化的网格表示
    grid_length = int(truck_dims[0] * 2)  # 每0.5m一个单位
    grid_width = int(truck_dims[1] * 2)
    
    # 初始化网格
    grid = [['.' for _ in range(grid_length)] for _ in range(grid_width)]
    
    # 在网格中标记货物位置
    for cargo in solution.cargo_instances:
        start_x = int(cargo.x * 2)
        start_y = int(cargo.y * 2)
        end_x = int((cargo.x + cargo.length) * 2)
        end_y = int((cargo.y + cargo.width) * 2)
        
        for y in range(start_y, min(end_y, grid_width)):
            for x in range(start_x, min(end_x, grid_length)):
                if y < len(grid) and x < len(grid[y]):
                    grid[y][x] = cargo.cargo_type
    
    # 打印网格
    print("   ", end="")
    for i in range(0, grid_length, 4):
        print(f"{i//2:2}", end="  ")
    print()
    
    for y, row in enumerate(grid):
        print(f"{y//2:2.1f} ", end="")
        for x, cell in enumerate(row):
            if x % 2 == 0:
                print(cell, end="")
            else:
                print(" ", end="")
        print()

def analyze_solution_performance(solutions):
    """分析解决方案性能"""
    print("\n" + "="*70)
    print("解决方案性能分析")
    print("="*70)
    
    # 货车信息
    trucks = {
        'Type1': (10.0, 2.5, 2.8, 5000, 1000),
        'Type2': (12.0, 3.0, 3.0, 6000, 1500),
        'Type3': (8.0, 2.0, 2.5, 4000, 800)
    }
    
    total_cost = sum(sol.total_cost for sol in solutions)
    total_weight = sum(sol.total_weight for sol in solutions)
    total_volume_used = 0
    total_volume_available = 0
    
    print(f"总体指标:")
    print(f"  总运输费用: {total_cost} 元")
    print(f"  使用货车数量: {len(solutions)} 辆")
    print(f"  总载重: {total_weight} kg")
    
    # 计算空间利用率
    for solution in solutions:
        truck_info = trucks[solution.truck_type]
        truck_volume = truck_info[0] * truck_info[1] * truck_info[2]
        total_volume_available += truck_volume
        
        cargo_volume = sum(c.length * c.width * c.height for c in solution.cargo_instances)
        total_volume_used += cargo_volume
    
    space_utilization = total_volume_used / total_volume_available * 100
    print(f"  总体空间利用率: {space_utilization:.1f}%")
    
    # 分析每辆货车
    print(f"\n各货车详细分析:")
    for i, solution in enumerate(solutions, 1):
        truck_info = trucks[solution.truck_type]
        truck_volume = truck_info[0] * truck_info[1] * truck_info[2]
        cargo_volume = sum(c.length * c.width * c.height for c in solution.cargo_instances)
        weight_utilization = solution.total_weight / truck_info[3] * 100
        volume_utilization = cargo_volume / truck_volume * 100
        
        print(f"\n  货车 {i} ({solution.truck_type}):")
        print(f"    货车规格: {truck_info[0]}×{truck_info[1]}×{truck_info[2]}m, {truck_info[3]}kg")
        print(f"    使用费用: {solution.total_cost} 元")
        print(f"    载重利用率: {weight_utilization:.1f}% ({solution.total_weight}/{truck_info[3]} kg)")
        print(f"    空间利用率: {volume_utilization:.1f}% ({cargo_volume:.1f}/{truck_volume:.1f} m³)")
        
        # 货物统计
        cargo_count = {}
        for cargo in solution.cargo_instances:
            cargo_type = cargo.cargo_type
            cargo_count[cargo_type] = cargo_count.get(cargo_type, 0) + 1
        
        print(f"    装载货物: ", end="")
        for cargo_type, count in cargo_count.items():
            print(f"{cargo_type}类{count}件 ", end="")
        print()

def analyze_alternative_solutions():
    """分析可能的替代方案"""
    print("\n" + "="*70)
    print("可能的替代方案分析")
    print("="*70)
    
    # 分析不同货车组合的理论成本
    print("不同货车组合的理论分析:")
    
    combinations = [
        ("3辆Type3", 3 * 800, "适合小批量、多批次运输"),
        ("1辆Type1 + 1辆Type2", 1000 + 1500, "混合载重能力"),
        ("2辆Type1", 2 * 1000, "中等载重方案"),
        ("2辆Type2", 2 * 1500, "当前采用方案"),
        ("1辆Type2 + 1辆Type3", 1500 + 800, "载重+成本平衡")
    ]
    
    print("\n可能的货车组合方案:")
    for combo, cost, desc in combinations:
        if cost == 3000:
            status = "★ 当前方案"
        elif cost < 3000:
            status = "◆ 可能更优"
        else:
            status = "◇ 成本较高"
        print(f"  {combo:20} {cost:4}元 {status} - {desc}")
    
    print("\n注意: 实际可行性还需要考虑空间和重量约束")

def generate_optimization_suggestions():
    """生成优化建议"""
    print("\n" + "="*70)
    print("优化建议")
    print("="*70)
    
    suggestions = [
        "算法改进建议:",
        "1. 引入遗传算法或模拟退火算法进行全局优化",
        "2. 实现更精确的3D装箱算法，如底左填充(BLF)算法",
        "3. 考虑货物装载的稳定性和重心分布",
        "4. 加入时间窗口约束和路径优化",
        "",
        "实际应用建议:",
        "1. 建立货物预处理和分类系统",
        "2. 考虑装卸作业的便利性",
        "3. 预留一定的安全空间避免损坏",
        "4. 建立动态调度系统应对订单变化",
        "",
        "成本优化建议:",
        "1. 考虑租赁vs购买不同类型货车",
        "2. 建立货车使用效率监控系统",
        "3. 优化货车维护和调度计划",
        "4. 考虑与其他物流企业的协同配送"
    ]
    
    for suggestion in suggestions:
        print(f"  {suggestion}")

def main():
    """主函数"""
    print("开始生成物流优化详细分析报告...")
    
    # 求解优化问题
    optimizer = LogisticsOptimizer()
    solutions = optimizer.solve()
    
    if not solutions:
        print("未找到可行解决方案！")
        return
    
    # 打印基本解决方案
    optimizer.print_solution(solutions)
    
    # 生成ASCII布局图
    for i, solution in enumerate(solutions, 1):
        generate_ascii_layout(solution, i)
    
    # 性能分析
    analyze_solution_performance(solutions)
    
    # 替代方案分析
    analyze_alternative_solutions()
    
    # 优化建议
    generate_optimization_suggestions()
    
    print("\n" + "="*70)
    print("分析报告生成完成！")
    print("="*70)

if __name__ == "__main__":
    main()