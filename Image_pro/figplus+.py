from cv2 import imread, EVENT_LBUTTONDOWN, circle, EVENT_RBUTTONDOWN, \
imshow, namedWindow, setMouseCallback, waitKey, destroyAllWindows, cvtColor, COLOR_BGR2RGB
import math
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from matplotlib import pyplot as plt

class MeasurementTool:
    def __init__(self):
        self.image_path = ''
        self.image = None
        self.points = []
        self.distance_pixels = []
        self.distance_pixel = None
        self.actual_headlength_cm = None
        self.actual_bodylength_cm = None
        self.measurements_df = None
        self.pixels_to_length_ratio = 1
        self.file_path = None

        self.root = tk.Tk()
        self.root.geometry("600x400")
        self.label = tk.Label(self.root, text="图片路径:")
        self.label.pack()
        self.image_path_text_widget = tk.Text(self.root, height=1.5)
        self.image_path_text_widget.pack()
        self.select_image_button = tk.Button(self.root, text="选择图片", command=self.select_image)
        self.select_image_button.pack()

        # 添加用于设置像素到长度比例的文本输入和按钮
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

        self.monitor_text_widget = tk.Text(self.root, height=10)
        self.monitor_text_widget.pack()

        self.root.mainloop()

    def select_image(self):
        if self.image_path:
            pass
        else:
            self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
            self.image_path_text_widget.insert(tk.END, self.image_path)
            self.image = imread(self.image_path)

    def set_pixels_to_length_ratio(self):
        ratio_text = self.ratio_entry.get()
        try:
            self.pixels_to_length_ratio = float(ratio_text)
            self.print_to_monitor("像素到长度比例已设置为: {}".format(self.pixels_to_length_ratio))
        except ValueError:
            self.print_to_monitor("无效的比例值")

    def mouse_callback(self, event, x, y, flags, param):
        if event == EVENT_LBUTTONDOWN:
            circle(self.image, (x, y), 5, (0, 255, 0), -1)
            self.points.append((x, y))
            imshow('image', self.image)
        elif event == EVENT_RBUTTONDOWN:  # Right mouse button click to undo the last point
            if self.points:
                self.points.pop()
                self.image = imread(self.image_path)  # Reset image to original state
                for point in self.points:
                    circle(self.image, point, 5, (0, 255, 0), -1)
                imshow('image', self.image)

    def perform_measurement(self):
        namedWindow('image')
        setMouseCallback('image', self.mouse_callback)

        while True:
            imshow('image', self.image)
            if waitKey(1) & 0xFF != 255:
                if len(self.points) == 2:
                    break
                else:
                    self.print_to_monitor("选择的点的数量存在问题")
                    pass
            else:
                pass

        destroyAllWindows()

        self.distance_pixel = self.calculate_distance(self.points[0], self.points[1])
        self.distance_pixels.append(self.distance_pixel)
        self.print_to_monitor("Distance in pixels: {}".format(self.distance_pixel))
        self.points = []
        if len(self.distance_pixels) == 5:
            self.actual_headlength_cm = ((self.distance_pixels[1] / self.distance_pixels[0]) * self.pixels_to_length_ratio) * (
                        self.distance_pixels[3] / self.distance_pixels[2])
            self.print_to_monitor("Actual headLength: {} cm".format(self.actual_headlength_cm))
            self.actual_bodylength_cm = ((self.distance_pixels[1] / self.distance_pixels[0]) * self.pixels_to_length_ratio) * (
                        self.distance_pixels[4] / self.distance_pixels[2])
            self.print_to_monitor("Actual bodyLength: {} cm".format(self.actual_bodylength_cm))

    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def save_measurement(self):
        # Append measurements to the DataFrame as a new row
        self.file_path = filedialog.askdirectory()
        new_row = {"Actual headLength(cm):": self.actual_headlength_cm,
                   "Actual bodyLength (cm)": self.actual_bodylength_cm}
        self.measurements_df = pd.concat([self.measurements_df, pd.DataFrame([new_row])], ignore_index=True)
        self.measurements_df.to_csv(self.file_path + '/measurement.csv', index=False)
        self.print_to_monitor("测量结果已保存！")

    def show_image(self):
        plt.imshow(cvtColor(self.image, COLOR_BGR2RGB))
        plt.axis('off')

    def run(self):
        for i in range(5):
            self.print_to_monitor("Measurement {}".format(i + 1))
            self.perform_measurement()
            self.show_image()

    def print_to_monitor(self, message):
        self.monitor_text_widget.insert(tk.END, message + "\n")
        self.monitor_text_widget.see(tk.END)  # Scroll to the end

    def write(self, text):
        self.monitor_text_widget.insert(tk.END, text)

a = MeasurementTool()

a.run()
