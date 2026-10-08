import cv2
import numpy as np

# 创建一个200x200的黑色图片
img = np.zeros((200, 200, 3), dtype=np.uint8)

# 在图片中间画一个白色的方块作为测试目标
cv2.rectangle(img, (50, 50), (150, 150), (255, 255, 255), -1)

# 保存图片
cv2.imwrite('plot_seg_visual/test_data/images/test_image.jpg', img)
print('测试图片创建成功！')