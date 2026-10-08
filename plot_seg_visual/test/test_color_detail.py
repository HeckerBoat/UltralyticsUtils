#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
详细测试颜色分配逻辑，检查预定义颜色和生成颜色
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

from plot_seg_visual import get_colors

def test_predefined_colors():
    """测试预定义颜色列表是否有重复"""
    print("检查预定义颜色列表...")
    print("=" * 60)
    
    # 直接检查预定义颜色列表
    predefined_colors = [
        (0, 0, 255),   # 红色
        (0, 255, 0),   # 绿色
        (255, 0, 0),   # 蓝色
        (0, 255, 255), # 黄色
        (255, 0, 255), # 洋红色
        (255, 255, 0), # 青色
        (128, 0, 0),   # 深红色
        (128, 128, 0), # 橄榄色
        (0, 128, 0),   # 深绿色
        (128, 0, 128), # 紫色
        (0, 128, 128), # 蓝绿色
        (0, 0, 128),   # 深蓝色
        (255, 165, 0), # 橙色
        (192, 192, 192),# 银色
        (128, 128, 128),# 灰色
        (255, 255, 255),# 白色
        (139, 0, 0),   # 深红色
        (0, 100, 0),   # 深绿色
        (0, 0, 139),   # 深蓝色
        (139, 139, 0)  # 暗黄色
    ]
    
    print(f"预定义颜色数量: {len(predefined_colors)}")
    unique_predefined = set(predefined_colors)
    print(f"唯一预定义颜色数量: {len(unique_predefined)}")
    
    if len(unique_predefined) < len(predefined_colors):
        print("警告: 预定义颜色列表中存在重复颜色!")
        # 找出重复的颜色
        seen = set()
        duplicates = set()
        for color in predefined_colors:
            if color in seen:
                duplicates.add(color)
            else:
                seen.add(color)
        print(f"重复的颜色: {duplicates}")
    else:
        print("预定义颜色列表中没有重复颜色。")
    
    print()

def test_color_generation():
    """测试颜色生成并显示所有颜色"""
    print("测试颜色生成并显示所有颜色...")
    print("=" * 60)
    
    # 测试生成25个颜色（超过预定义颜色数量）
    num_colors = 25
    colors = get_colors(num_colors)
    
    print(f"生成了 {len(colors)} 个颜色:")
    for i, color in enumerate(colors):
        print(f"  类别 {i}: {color}")
    
    # 检查是否有重复
    unique_colors = set(colors)
    print(f"\n唯一颜色数量: {len(unique_colors)}")
    
    if len(unique_colors) == num_colors:
        print("所有颜色都是唯一的!")
    else:
        print("错误: 存在重复颜色!")
    
    print()

def test_pink_colors():
    """特别检查粉色相关颜色"""
    print("特别检查粉色相关颜色...")
    print("=" * 60)
    
    # 生成足够多的颜色
    colors = get_colors(50)
    
    # 查找粉色系颜色（R > G and R > B，且G和B较小）
    pink_colors = []
    for i, color in enumerate(colors):
        b, g, r = color  # BGR格式
        if r > g and r > b and g < 150 and b < 150:
            pink_colors.append((i, color))
    
    print(f"找到 {len(pink_colors)} 个粉色系颜色:")
    for idx, color in pink_colors:
        print(f"  类别 {idx}: {color}")
    
    if len(pink_colors) > 1:
        print("注意: 存在多个粉色系颜色，可能会被视为重复。")
    else:
        print("粉色系颜色唯一。")
    
    print()

if __name__ == "__main__":
    test_predefined_colors()
    test_color_generation()
    test_pink_colors()
    print("=" * 60)
    print("详细测试完成！")
