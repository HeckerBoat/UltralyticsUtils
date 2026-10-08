import cv2
import numpy as np

# 创建一个100x100的黑色图片
img = np.zeros((100, 100, 3), dtype=np.uint8)

# 保存图片
cv2.imwrite('test_images/images/test.jpg', img)
print('测试图片创建成功：test_images/images/test.jpg')