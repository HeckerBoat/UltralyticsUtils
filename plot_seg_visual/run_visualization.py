import argparse
import os
import sys
import subprocess


def main():
    """
    分割掩码可视化工具命令行入口
    """
    parser = argparse.ArgumentParser(description='分割掩码可视化工具')
    parser.add_argument('--img_path', type=str, default='./', 
                        help='数据集路径，包含images和labels文件夹')
    parser.add_argument('--cls_path', type=str, default='./classes.txt', 
                        help='类别文件路径，如classes.txt')
    parser.add_argument('--bg_ground', type=str, default='black', 
                        choices=['black', 'img'],
                        help=fr'背景类型：black（黑色背景）或img（原图背景）')
    parser.add_argument('--class_color', type=str, default='white', 
                        choices=['auto', 'white'],
                        help=fr'类别颜色：auto（不同类别不同颜色）或white（统一白色）')
    
    args = parser.parse_args()
    
    # 验证参数
    if not os.path.exists(args.img_path):
        print(f"错误：数据集路径不存在: {args.img_path}")
        sys.exit(1)
    
    if not os.path.exists(args.cls_path):
        print(f"错误：类别文件不存在: {args.cls_path}")
        sys.exit(1)
    
    img_dir = os.path.join(args.img_path, 'images')
    txt_dir = os.path.join(args.img_path, 'labels')
    
    if not os.path.exists(img_dir):
        print(f"错误：images文件夹不存在: {img_dir}")
        sys.exit(1)
    
    if not os.path.exists(txt_dir):
        print(f"错误：labels文件夹不存在: {txt_dir}")
        sys.exit(1)
    
    # 构建命令，使用绝对路径
    command = [
        sys.executable, 'backend/plot_seg_visual.py',
        '--img_path', os.path.abspath(args.img_path),
        '--cls_path', os.path.abspath(args.cls_path),
        '--bg_ground', args.bg_ground,
        '--class_color', args.class_color
    ]
    
    print("开始运行分割掩码可视化...")
    print(f"数据集路径: {args.img_path}")
    print(f"类别文件: {args.cls_path}")
    print(f"背景类型: {args.bg_ground}")
    print(f"类别颜色: {args.class_color}")
    print(f"执行命令: {' '.join(command)}")
    print("=" * 60)
    
    try:
        # 设置工作目录为项目根目录
        project_root = os.path.dirname(os.path.abspath(__file__))
        # 运行命令，捕获原始字节输出
        result = subprocess.run(command, capture_output=True, text=False, cwd=project_root)
        
        # 显示输出，使用utf-8编码解码
        if result.stdout:
            try:
                print(result.stdout.decode('utf-8', errors='replace'))
            except Exception as e:
                print(f"解码标准输出失败: {str(e)}")
        
        if result.stderr:
            try:
                print(f"错误输出: {result.stderr.decode('utf-8', errors='replace')}")
            except Exception as e:
                print(f"解码错误输出失败: {str(e)}")
        
        if result.returncode == 0:
            print("=" * 60)
            print("分割掩码可视化完成！")
            print(f"结果保存到: {os.path.join(args.img_path, 'masks')}")
        else:
            print(f"运行失败，返回码: {result.returncode}")
            sys.exit(1)
    except Exception as e:
        print(f"错误：{str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
