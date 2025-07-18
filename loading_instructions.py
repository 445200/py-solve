#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
货物装载指导说明生成器

为装货工人提供详细的装载步骤和注意事项
"""

from logistics_optimization import LogisticsOptimizer

def generate_loading_instructions(solutions):
    """生成详细的装货指导说明"""
    print("="*80)
    print("📦 货物装载操作指导书")
    print("="*80)
    
    # 货车尺寸说明
    trucks_info = {
        'Type1': (10.0, 2.5, 2.8, 5000),
        'Type2': (12.0, 3.0, 3.0, 6000),
        'Type3': (8.0, 2.0, 2.5, 4000)
    }
    
    for truck_idx, solution in enumerate(solutions, 1):
        truck_info = trucks_info[solution.truck_type]
        
        print(f"\n🚛 货车 {truck_idx} ({solution.truck_type}) 装载指导")
        print("-" * 60)
        print(f"货车规格: 长{truck_info[0]}m × 宽{truck_info[1]}m × 高{truck_info[2]}m")
        print(f"最大载重: {truck_info[3]}kg")
        print(f"实际装载重量: {solution.total_weight}kg")
        print(f"重量余量: {truck_info[3] - solution.total_weight}kg")
        
        # 按装载顺序排序（从底层到高层，从前到后）
        sorted_cargo = sorted(solution.cargo_instances, 
                            key=lambda x: (x.z, x.x, x.y))
        
        print(f"\n📋 装载步骤（共{len(sorted_cargo)}件货物）:")
        
        for step, cargo in enumerate(sorted_cargo, 1):
            rotation_note = "⚠️ 需要旋转90° (长宽交换)" if cargo.rotated else "✅ 正常方向"
            
            print(f"\n  步骤 {step:2d}: 装载 {cargo.cargo_type}_{cargo.instance_id}")
            print(f"          🎯 目标位置: 货车内({cargo.x:.1f}, {cargo.y:.1f}, {cargo.z:.1f})")
            print(f"          📏 货物尺寸: {cargo.length:.1f}m(长) × {cargo.width:.1f}m(宽) × {cargo.height:.1f}m(高)")
            print(f"          ⚖️  货物重量: {cargo.weight}kg")
            print(f"          🔄 摆放方向: {rotation_note}")
            
            # 具体装载指导
            if cargo.z == 0:
                print(f"          💡 操作提示: 直接放置在货车底板上")
            else:
                print(f"          💡 操作提示: 堆叠在高度{cargo.z:.1f}m的货物上方")
            
            # 位置指导
            print(f"          📍 精确定位:")
            print(f"             - 距离货车前端: {cargo.x:.1f}m")
            print(f"             - 距离货车左侧: {cargo.y:.1f}m") 
            print(f"             - 距离货车底板: {cargo.z:.1f}m")
            print(f"             - 占用空间: 长{cargo.x:.1f}~{cargo.x + cargo.length:.1f}m, "
                  f"宽{cargo.y:.1f}~{cargo.y + cargo.width:.1f}m, "
                  f"高{cargo.z:.1f}~{cargo.z + cargo.height:.1f}m")

def generate_safety_notes():
    """生成安全注意事项"""
    print(f"\n⚠️  安全注意事项")
    print("-" * 40)
    safety_notes = [
        "1. 装载前请检查货车状态，确保底板平整、无杂物",
        "2. 重货在下，轻货在上，保持重心稳定",
        "3. 按照指定坐标精确摆放，避免货物倾斜或悬空",
        "4. 货物间预留适当间隙，便于固定和通风",
        "5. 使用绳索、护角等工具固定货物，防止运输中移位",
        "6. 装载完成后检查车厢门能否正常关闭",
        "7. 确认总重量未超过车辆最大载重",
        "8. 易碎货物要特别标记和保护"
    ]
    
    for note in safety_notes:
        print(f"   {note}")

def generate_cargo_summary(solutions):
    """生成货物装载汇总表"""
    print(f"\n📊 货物装载汇总表")
    print("-" * 60)
    
    # 所有货物信息
    all_cargo_info = {
        'A': {'size': '3.0×2.0×1.5m', 'weight': '800kg', 'desc': 'A类电子产品'},
        'B': {'size': '2.5×2.0×2.0m', 'weight': '1000kg', 'desc': 'B类电子产品'},  
        'C': {'size': '4.0×1.5×1.0m', 'weight': '500kg', 'desc': 'C类电子产品'}
    }
    
    total_items = 0
    total_weight = 0
    
    for truck_idx, solution in enumerate(solutions, 1):
        print(f"\n货车 {truck_idx} 装载清单:")
        cargo_count = {}
        for cargo in solution.cargo_instances:
            cargo_type = cargo.cargo_type
            cargo_count[cargo_type] = cargo_count.get(cargo_type, 0) + 1
        
        truck_items = 0
        truck_weight = 0
        for cargo_type, count in sorted(cargo_count.items()):
            info = all_cargo_info[cargo_type]
            item_weight = count * int(info['weight'].replace('kg', ''))
            truck_items += count
            truck_weight += item_weight
            print(f"  {cargo_type}类: {count}件 × {info['weight']} = {item_weight}kg ({info['desc']})")
        
        print(f"  小计: {truck_items}件, {truck_weight}kg")
        total_items += truck_items
        total_weight += truck_weight
    
    print(f"\n总计: {total_items}件货物, {total_weight}kg")

def main():
    """主函数"""
    print("正在生成装货指导说明...")
    
    # 获取优化解决方案
    optimizer = LogisticsOptimizer()
    solutions = optimizer.solve()
    
    if not solutions:
        print("未找到可行解决方案！")
        return
    
    # 生成装载指导
    generate_loading_instructions(solutions)
    
    # 生成货物汇总
    generate_cargo_summary(solutions)
    
    # 生成安全注意事项
    generate_safety_notes()
    
    print(f"\n" + "="*80)
    print("📝 装货指导说明生成完成！请严格按照步骤执行装载操作。")
    print("="*80)

if __name__ == "__main__":
    main()