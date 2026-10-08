import numpy as np
import matplotlib.pyplot as plt
import trimesh
from scipy.ndimage import median_filter
from PIL import Image

def read_glb_file(file_path):
    """读取 GLB 文件并返回点云数据"""
    try:
        mesh = trimesh.load(file_path, force='mesh')
        if isinstance(mesh, trimesh.Scene):
            all_vertices = []
            for geom in mesh.geometry.values():
                if hasattr(geom, 'vertices') and len(geom.vertices) > 0:
                    all_vertices.append(geom.vertices)
            if all_vertices:
                vertices = np.vstack(all_vertices)
            else:
                vertices = np.array([])
        else:
            vertices = mesh.vertices if hasattr(mesh, 'vertices') else np.array([])
        return vertices
    except Exception as e:
        print(f"读取 GLB 文件时出错: {e}")
        return None

def project_to_depth_map(vertices, resolution=(512, 512), projection_type='orthographic'):
    """将点云投影到深度图"""
    if vertices is None or len(vertices) == 0:
        return None
    
    # 获取点云边界
    min_coords = vertices.min(axis=0)
    max_coords = vertices.max(axis=0)
    extent = max_coords - min_coords
    
    # 计算中心点
    center = (min_coords + max_coords) / 2
    
    # 创建深度图
    depth_map = np.full(resolution, np.nan, dtype=np.float32)
    
    # 投影类型选择
    if projection_type == 'orthographic':
        # 正交投影 (默认投影到 XOY 平面，Z 作为深度值)
        # 映射到图像坐标
        for v in vertices:
            x, y, z = v
            
            # 将坐标归一化到 [0, 1] 范围
            u = (x - min_coords[0]) / extent[0]
            v_coord = (y - min_coords[1]) / extent[1]  # 注意：v 是 Python 保留字，使用 v_coord
            
            # 映射到像素坐标
            pixel_u = int(u * (resolution[1] - 1))
            pixel_v = int(v_coord * (resolution[0] - 1))
            
            # 确保坐标在范围内
            if 0 <= pixel_u < resolution[1] and 0 <= pixel_v < resolution[0]:
                # 保留最近的点 (Z 值最小)
                if np.isnan(depth_map[pixel_v, pixel_u]) or z < depth_map[pixel_v, pixel_u]:
                    depth_map[pixel_v, pixel_u] = z
    else:
        print(f"不支持的投影类型: {projection_type}")
        return None
    
    return depth_map

def process_depth_map(depth_map, fill_holes=True, normalize=True):
    """处理深度图：填充空洞、归一化"""
    if depth_map is None:
        return None
    
    processed = depth_map.copy()
    
    # 填充空洞
    if fill_holes:
        # 简单的中值滤波填充
        mask = np.isnan(processed)
        processed[mask] = np.nanmin(processed)  # 用最小值填充空洞
        processed = median_filter(processed, size=3)
    
    # 归一化到 [0, 255]
    if normalize and not np.all(np.isnan(processed)):
        min_val = np.nanmin(processed)
        max_val = np.nanmax(processed)
        if max_val != min_val:
            processed = (processed - min_val) / (max_val - min_val) * 255
        processed = np.clip(processed, 0, 255).astype(np.uint8)
    
    return processed

def save_depth_map(depth_map, output_path):
    """保存深度图为图像文件"""
    if depth_map is None:
        print("无法保存：深度图为空")
        return False
    
    try:
        # 确保深度图是 uint8 类型
        if depth_map.dtype != np.uint8:
            depth_map = depth_map.astype(np.uint8)
        
        # 创建灰度图像
        img = Image.fromarray(depth_map, mode='L')
        img.save(output_path)
        print(f"深度图已保存至: {output_path}")
        return True
    except Exception as e:
        print(f"保存深度图时出错: {e}")
        return False

def visualize_depth_map(depth_map, title="深度图"):
    """可视化深度图"""
    if depth_map is None:
        print("无法可视化：深度图为空")
        return
    
    plt.figure(figsize=(10, 8))
    plt.imshow(depth_map, cmap='viridis')
    plt.colorbar(label='深度值')
    plt.title(title)
    plt.axis('equal')
    plt.show()

if __name__ == "__main__":
    # 参数设置
    glb_file_path = "./1.glb"  # 替换为实际的 GLB 文件路径
    output_image_path = "./depth_map.png"
    image_resolution = (512, 512)  # 深度图分辨率
    
    # 执行处理流程
    vertices = read_glb_file(glb_file_path)
    if vertices is not None:
        print(f"成功加载点云，包含 {len(vertices)} 个点")
        
        depth_map = project_to_depth_map(vertices, resolution=image_resolution)
        processed_depth_map = process_depth_map(depth_map)
        
        if processed_depth_map is not None:
            save_depth_map(processed_depth_map, output_image_path)
            visualize_depth_map(processed_depth_map)
        else:
            print("处理深度图失败")
    else:
        print("加载点云失败")    