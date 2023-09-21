import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

# Tkinter界面获取图片路径
def open_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        selected_image_path = file_path
        image_label.config(text=f"已选择图片：{selected_image_path}")
        print("选择的路径是", selected_image_path)

# 显示图片
def show_image():
    if selected_image_path:
        img = cv2.imread(selected_image_path)
        if points_to_measure:
            for point in points_to_measure:
                cv2.circle(img, tuple(point), 5, (0, 255, 0), -1)
            cv2.imshow('image', img)

# 鼠标点击事件处理
def on_mouse_click(event, x, y, flags, param):
    global points_to_measure
    if event == cv2.EVENT_LBUTTONDOWN:  # 左键单击选择点
        points_to_measure.append((x, y))
        show_image()
    elif event == cv2.EVENT_RBUTTONDOWN:  # 右键单击撤销选择点
        if points_to_measure:
            points_to_measure.pop()
            show_image()

# 测量图像上两点之间的距离
def measure_distance():
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', on_mouse_click)
    img = cv2.imread(selected_image_path)
    cv2.imshow('image', img)
    key = cv2.waitKey(1) & 0xFF
    while len(points_to_measure) != 6 and key !=255:
        on_mouse_click
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    dis1 = np.linalg.norm(np.array(points_to_measure[1]) - np.array(points_to_measure[0]))  # 计算两点之间的欧氏距离
    dis2 = np.linalg.norm(np.array(points_to_measure[3]) - np.array(points_to_measure[2]))
    dis3 = np.linalg.norm(np.array(points_to_measure[5]) - np.array(points_to_measure[4]))
    print("dis1:", dis1)
    print("dis2:", dis2)
    print("dis3:", dis3)
    exc = float(input("Length of bar:"))
    real_length1 = exc*(float(dis2)/float(dis1))
    real_length2 = exc*(float(dis3)/float(dis1))
    # cv2.putText(img, f"{distance:.2f} 像素", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # 在图像上显示距离
    # cv2.imshow('带有距离的图像', img)
    print("头骨长度是：\t", real_length1)
    print("体长长度是:\t", real_length2)
    points_to_measure.clear()


if __name__ == "__main__":
    # 全局变量
    selected_image_path = None
    points_to_measure = []


    root = tk.Tk()
    root.title("一组头骨体长")

    image_label = tk.Label(root, text="未选择图片")
    image_label.pack(pady=10)

    btn_open_image = tk.Button(root, text="选择图片", command=open_image)
    btn_open_image.pack(pady=5)

    btn_open_image = tk.Button(root, text="运行", command=measure_distance)
    btn_open_image.pack(pady=0)

    root.mainloop()
