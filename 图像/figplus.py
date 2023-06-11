import cv2
import math
import csv
from matplotlib import pyplot as plt

class MeasurementTool:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)
        self.points = []
        self.distance_pixels = None
        self.actual_length_cm = None

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(self.image, (x, y), 5, (0, 255, 0), -1)
            self.points.append((x, y))
            cv2.imshow('image', self.image)

    def perform_measurement(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.mouse_callback)

        while True:
            cv2.imshow('image', self.image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

        if len(self.points) >= 2:
            self.distance_pixels = self.calculate_distance(self.points[0], self.points[1])
            print("Distance in pixels:", self.distance_pixels)

            pixels_to_length_ratio = 0.5
            self.actual_length_cm = self.distance_pixels * pixels_to_length_ratio
            print("Actual Length:", self.actual_length_cm, "cm")

    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def save_measurement(self, file_path):
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.distance_pixels, self.actual_length_cm])

    def show_image(self):
        plt.imshow(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()


# 创建 MeasurementTool 实例并进行 5 次测量
image_path = '333.png'
measurement_tool = MeasurementTool(image_path)

for i in range(5):
    print("Measurement", i+1)
    measurement_tool.perform_measurement()
    measurement_tool.save_measurement('measurement.csv')
    measurement_tool.show_image()
