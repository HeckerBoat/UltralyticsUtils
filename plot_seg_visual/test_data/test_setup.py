import os
import cv2
import numpy as np

# 创建测试目录结构
os.makedirs('test_images/images', exist_ok=True)
os.makedirs('test_images/labels', exist_ok=True)

# 创建测试图片
img = np.zeros((100, 100, 3), dtype=np.uint8)
cv2.imwrite('test_images/images/test.jpg', img)

# 创建类别文件
with open('test_images/classes.txt', 'w') as f:
    f.write('person\ncar\nbicycle\ndog\ncat')

# 创建标签文件
with open('test_images/labels/test.txt', 'w') as f:
    f.write('0 0.25 0.25 0.75 0.25 0.75 0.75 0.25 0.75\n')
    f.write('1 0.25 0.25 0.75 0.25 0.75 0.75 0.25 0.75\n')

print('测试环境搭建完成！')