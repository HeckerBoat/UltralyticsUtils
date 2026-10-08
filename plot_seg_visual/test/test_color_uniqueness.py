#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试颜色分配逻辑的唯一性
"""

import sys
import os

# 添加backend目录到Python路径
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend'))

from plot_seg_visual import get_colors

def test_color_uniqueness():
    """测试颜色分配的唯一性"""
    print("测试颜色分配逻辑的唯一性...")
    print("=" * 60)
    
    # 测试不同数量的颜色生成
    test_cases = [5, 20, 30, 50, 100]
    
    for case in test_cases:
        print(f"测试生成 {case} 个颜色:")
        colors = get_colors(case)
        
        # 检查颜色数量是否正确
        assert len(colors) == case, f"颜色数量错误: 期望 {case}, 实际 {len(colors)}"
        
        # 检查是否有重复颜色
        unique_colors = set(colors)
        assert len(unique_colors) == case, f"存在重复颜色: 期望 {case} 个唯一颜色, 实际 {len(unique_colors)} 个"
        
        # 打印前几个颜色作为示例
        print(f"  生成了 {len(colors)} 个颜色，前5个: {colors[:5]}")
        print(f"  所有颜色都是唯一的: ✓")
        print()
    
    print("=" * 60)
    print("所有测试通过！颜色分配逻辑正确，所有颜色都唯一。")

if __name__ == "__main__":
    test_color_uniqueness()
