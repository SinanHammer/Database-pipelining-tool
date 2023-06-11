import cv2
import math
import csv
from matplotlib import pyplot as plt

# 加载图像
image = cv2.imread('333.png')

# 创建一个回调函数来处理鼠标事件
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # 在点击位置绘制一个圆圈
        cv2.circle(image, (x, y), 5, (0, 255, 0), -1)
        # 将坐标添加到点列表中
        points.append((x, y))
        # 显示带有点击标记的图像
        cv2.imshow('image', image)

# 创建一个空的点列表来保存点击的坐标
points = []

# 创建一个窗口，并将回调函数与窗口绑定
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_callback)

# 在图像上等待直到按下 'q' 键
while True:
    cv2.imshow('image', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 关闭窗口
cv2.destroyAllWindows()

# 计算两点之间的距离
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# 检查是否至少选择了两个点
if len(points) >= 2:
    # 计算长度（假设像素之间的距离为实际长度）
    distance_pixels = calculate_distance(points[0], points[1])
    print("Distance in pixels:", distance_pixels)

    # 假设每个像素对应实际长度的比例为 0.1 厘米
    pixels_to_length_ratio = 0.5

    # 计算实际长度（厘米）
    actual_length_cm = distance_pixels * pixels_to_length_ratio
    print("Actual Length:", actual_length_cm, "cm")

    # 保存测量结果到CSV文件
    def save_measurement(distance_pixels, actual_length_cm, file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Distance in pixels', 'Actual Length (cm)'])
            writer.writerow([distance_pixels, actual_length_cm])

    # 保存测量结果
    save_measurement(distance_pixels, actual_length_cm, 'measurement.csv')

# 显示带有点击标记的图像
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()
