import cv2
import math
import csv
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt
import sys

class MeasurementTool:
    def __init__(self):
        self.image_path = ''
        self.image = None
        self.points = []
        self.distance_pixels = []
        self.distance_pixel = None
        self.actual_headlength_cm = None
        self.actual_bodylength_cm = None
        self.measurements_df = pd.DataFrame()
        self.pixels_to_length_ratio = 1
        self.file_path = None

        self.root = tk.Tk()
        self.root.title("图像测量程序")
        self.root.geometry("600x400")
        self.label = tk.Label(self.root, text="图片路径:")
        self.label.pack()
        self.image_path_text_widget = tk.Text(self.root, height=1.5)
        self.image_path_text_widget.pack()
        self.select_image_button = tk.Button(self.root, text="选择图片", command=self.select_image)
        self.select_image_button.pack()

        self.ratio_label = tk.Label(self.root, text="像素到长度的比例:")
        self.ratio_label.pack()
        self.ratio_entry = tk.Entry(self.root)
        self.ratio_entry.pack()
        self.set_ratio_button = tk.Button(self.root, text="设置比例", command=self.set_pixels_to_length_ratio)
        self.set_ratio_button.pack()

        self.measurement_button = tk.Button(self.root, text="测量", command=self.run)
        self.measurement_button.pack()
        self.save_button = tk.Button(self.root, text="保存测量结果", command=self.save_measurement)
        self.save_button.pack()

        self.stop_button = tk.Button(self.root, text="结束", command=self.stop_measurement)
        self.stop_button.pack()

        self.monitor_text_widget = tk.Text(self.root, height=10)
        self.monitor_text_widget.pack()

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        self.image_path_text_widget.insert(tk.END, self.image_path)
        self.image = cv2.imread(self.image_path)

    def set_pixels_to_length_ratio(self):
        ratio_text = self.ratio_entry.get()
        try:
            self.pixels_to_length_ratio = float(ratio_text)
            self.print_to_monitor("像素到长度比例已设置为: {}".format(self.pixels_to_length_ratio))
        except ValueError:
            self.print_to_monitor("无效的比例值")

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.image, (x, y), 5, (0, 255, 0), -1)
            self.points.append((x, y))
            cv2.imshow('image', self.image)
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.points:
                self.points.pop()
                self.image = cv2.imread(self.image_path)
                for point in self.points:
                    cv2.circle(self.image, point, 5, (0, 255, 0), -1)
                cv2.imshow('image', self.image)

    def perform_measurement(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.mouse_callback)

        while True:
            cv2.imshow('image', self.image)
            if cv2.waitKey(1) & 0xFF != 255:
                if len(self.points) == 2:
                    break
                else:
                    self.print_to_monitor("选择的点的数量存在问题")
                    pass
            else:
                pass

        cv2.destroyAllWindows()

        self.distance_pixel = self.calculate_distance(self.points[0], self.points[1])
        self.distance_pixels.append(self.distance_pixel)
        self.print_to_monitor("像素距离: {}".format(self.distance_pixel))
        self.points = []
        if len(self.distance_pixels) == 5:
            self.actual_headlength_cm = ((self.distance_pixels[1] / self.distance_pixels[0]) * self.pixels_to_length_ratio) * (
                        self.distance_pixels[3] / self.distance_pixels[2])
            self.print_to_monitor("实际头长: {} cm".format(self.actual_headlength_cm))
            self.actual_bodylength_cm = ((self.distance_pixels[1] / self.distance_pixels[0]) * self.pixels_to_length_ratio) * (
                        self.distance_pixels[4] / self.distance_pixels[2])
            self.print_to_monitor("实际体长: {} cm".format(self.actual_bodylength_cm))

    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def save_measurement(self):
        self.file_path = filedialog.askdirectory()
        new_row = {"实际头长(cm)": self.actual_headlength_cm,
                   "实际体长(cm)": self.actual_bodylength_cm}
        self.measurements_df = pd.concat([self.measurements_df, pd.DataFrame([new_row])], ignore_index=True)
        self.measurements_df.to_csv(self.file_path + '/measurement.csv', index=False)
        self.print_to_monitor("测量结果已保存！")

    def show_image(self):
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.axis('off')

    def run(self):
        for i in range(5):
            self.print_to_monitor("测量 {}".format(i + 1))
            self.perform_measurement()
            self.show_image()
        self.root.mainloop()

    def print_to_monitor(self, message):
        self.monitor_text_widget.insert(tk.END, message + "\n")
        self.monitor_text_widget.see(tk.END)

    def stop_measurement(self):
        self.root.destroy()

    def write(self, text):
        self.monitor_text_widget.insert(tk.END, text)


