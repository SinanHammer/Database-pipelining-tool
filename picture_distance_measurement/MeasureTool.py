import cv2
from math import sqrt
from pandas import DataFrame
from copy import deepcopy
from tkinter import filedialog, Label, Text, Tk, Button, Menu, Entry, IntVar, Radiobutton, END
from tkinter.font import Font
from tkinter.messagebox import askyesno, showinfo



class MeasurementTool(object):
    def __init__(self, root):
        self.image_path = ''
        self.image = None
        self.image_line = None
        self.points = []
        self.distance_pixels = []
        self.distance_pixel = None
        self.actual_headlength_cm = None
        self.actual_bodylength_cm = None
        self.measurements_df = DataFrame(columns=["Actual headLength(cm)", "Actual bodyLength (cm)"])
        self.pixels_to_length_ratio = 1
        self.file_path = None
        self.loop_judgment = False

        # 对UI界面内容进行设置
        self.root = root
        self.root.geometry("600x400")
        self.root.title("Dinosaur Measurement")
        self.root.iconbitmap(f'./1.ico')
        self.root.resizable(True, True)
        self.custom_font = Font(family="Helvetica", size=12)
        self.label = Label(self.root, text=" 图  片  路  径: ", font=self.custom_font)
        self.label.place(x=10, y=38)
        self.image_path_text_widget = Text(self.root, height=1.4, width=36)
        self.image_path_text_widget.place(x=150, y=39)
        self.select_image_button = Button(self.root, text="选择图片", command=self.select_image)
        self.select_image_button.place(x=456, y=37)

        # 对菜单栏进行设置
        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="关于", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="教程", command=lambda: showinfo("Dinosaur Measurement Tutorial",'腾讯文档：https://docs.qq.com/doc/DZk5PbHJNUE9QZ1Ja'))
        self.file_menu.add_command(label="软件信息", command=lambda: showinfo('Dinosaur Measurement',
                                                                    '作者：孙建昊\n'
                                                                    '导师：陈中强 & 黄元耕\n'
                                                                    '单位：中国地质大学生物地质与环境地质国家重点实验室\n'
                                                                    '版本：1.0\n'
                                                                    '联系方式1：571979568@qq.com\n'
                                                                    '联系方式2：jianhaosun@cug.edu.cn'))
        self.root.config(menu=self.menu_bar)

        self.ratio_label = Label(self.root, text="Length of bar (cm):", font=self.custom_font)
        self.ratio_label.place(x=10, y=85)
        self.ratio_entry = Entry(self.root, width=41)
        self.ratio_entry.place(x=150, y=85)
        self.set_ratio_button = Button(self.root, text="设置比例", command=self.set_pixels_to_length_ratio)
        self.set_ratio_button.place(x=456, y=85)

        self.var = IntVar()
        self.var.set(0)
        self.choose_label = Label(self.root, text='测量模式:', font=self.custom_font)
        self.choose_label.place(x=10, y=130)
        self.choose_button1 = Radiobutton(self.root, text="模式一", variable=self.var, value=1)
        self.choose_button1.place(x=90, y=130)
        self.choose_button2 = Radiobutton(self.root, text="模式二", variable=self.var, value=2)
        self.choose_button2.place(x=180, y=130)
        self.choose_button3 = Radiobutton(self.root, text="模式三", variable=self.var, value=3)
        self.choose_button3.place(x=260, y=130)
        self.module_type = None
        self.measurement_button = Button(self.root, text=" 测    量 ", command=self.run)
        self.measurement_button.place(x=456, y=130)

        self.monitor_text_widget = Text(self.root, height=10, width=70)
        self.monitor_text_widget.place(x=10, y=200)

        self.root.bind('<Key>', self.key_press)

        self.root.protocol('WM_DELETE_WINDOW', self.StopAll)

        self.reset_button = Button(self.root, text=" 重    置 ", command=self.reset_all)
        self.reset_button.place(x=356, y=130)



    # 点击选择导入图片
    def select_image(self):
        if self.image_path:
            self.image_path = None
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        self.image_path_text_widget.insert(END, self.image_path)
        if self.image_path:
            self.print_to_monitor(f"成功获取图片!\n{self.image_path}")
        self.image = cv2.imread(self.image_path)
        self.image_line = deepcopy(self.image)

    # 设置比例尺的Bar的长度
    def set_pixels_to_length_ratio(self):
        ratio_text = self.ratio_entry.get()
        try:
            self.pixels_to_length_ratio = float(ratio_text)
            self.print_to_monitor("Length of bar已设置为: {}".format(self.pixels_to_length_ratio))
        except ValueError:
            self.print_to_monitor("无效的比例值,请重新进行设置!(eg：5)")

    # 对于鼠标左右键的操作进行设置
    def mouse_callback(self, event, x, y, flags, param):
        # 对左键进行设置，功能为单击选中
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_line = cv2.circle(self.image_line, (x, y), 5, (0, 255, 0), -1)
            self.points.append((x, y))
            self.structure_line(self.image_line, self.points)
            cv2.imshow('image', self.image_line)
        # 对鼠标的右键进行设置，功能为撤销
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.points:
                self.image_line = deepcopy(self.image)
                self.points.pop()
                for point in self.points:
                    self.image_line = cv2.circle(self.image_line, point, 5, (0, 255, 0), -1)
                self.structure_line(self.image_line, self.points)
                cv2.imshow('image', self.image_line)

    # 构建连线
    def structure_line(self, img, point):
        if len(point)%2 == 0:
            for i in range(0, len(point), 2):
                img = cv2.line(img, point[i], point[i+1], (0, 0, 255), 2)
            self.image_line = img
        else:
            point_copy = deepcopy(self.points[:-1])
            if int(len(point_copy)) == 0:
                pass
            else:
                for i in range(0, len(point_copy), 2):
                    img = cv2.line(img, point_copy[i], point_copy[i+1], (0, 0, 255), 2)
                self.image_line = img

    # 进行测量相关的操作
    def perform_measurement(self):
        cv2.namedWindow('image', cv2.WINDOW_FREERATIO)
        cv2.setMouseCallback('image', self.mouse_callback)

        while True:
            cv2.imshow('image', self.image_line)
            key = cv2.waitKey(1) & 0xFF
            if key != 255:
                if key == ord('q') or key == 27:
                    self.loop_judgment = True
                    cv2.destroyAllWindows()
                    break
                if len(self.points) == 2:
                    break
                else:
                    self.print_to_monitor("选择的点的数量存在问题!")
                    pass
            else:
                pass

        cv2.destroyAllWindows()

        self.distance_pixel = self.calculate_distance(self.points[0], self.points[1])
        self.distance_pixels.append(self.distance_pixel)
        self.print_to_monitor("Distance in pixels: {}".format(self.distance_pixel))
        self.points = []

    # 距离计算
    def calculate_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def print_to_monitor(self, message):
        self.monitor_text_widget.insert(END, message + "\n")  # 将消息追加到文本末尾
        self.monitor_text_widget.see(END)

    # 重置
    def reset_all(self):
        self.image_path = ''
        self.image_path_text_widget.delete("1.0", END)
        self.ratio_entry.delete(0, END)
        self.var.set(0)
        self.image = None
        self.loop_judgment = False
        self.points = []
        self.distance_pixels = []
        self.distance_pixel = None
        self.actual_headlength_cm = None
        self.actual_bodylength_cm = None
        self.measurements_df = DataFrame(columns=["Actual headLength(cm)", "Actual bodyLength (cm)"])
        self.pixels_to_length_ratio = 1
        self.file_path = None
        self.monitor_text_widget.delete("1.0", END)

    def key_press(self, event):
        if event.keysym == 'Escape':
            self.root.quit()

    # 程序运行
    def run(self):
        monitor = False
        self.module_type = int(self.var.get())
        self.print_to_monitor(f"已选择模式 {self.module_type}")
        if self.module_type == 0:
            self.print_to_monitor("请选择测量的模式！")
            monitor = False
        elif self.module_type == 1:
            for i in range(5):
                if self.loop_judgment:
                    break
                self.print_to_monitor("Measurement {}".format(i + 1))
                self.perform_measurement()
            monitor = True
        elif self.module_type == 2:
            for i in range(3):
                if self.loop_judgment:
                    break
                self.print_to_monitor("Measurement {}".format(i + 1))
                self.perform_measurement()
            monitor = True
        elif self.module_type == 3:
            for i in range(2):
                if self.loop_judgment:
                    break
                self.print_to_monitor("Measurement {}".format(i + 1))
                self.perform_measurement()
            monitor = True
        else:
            self.print_to_monitor("-操作存在问题，请反馈开发者处理！")
            monitor = False

        if monitor:
            if len(self.distance_pixels) == 5:
                self.actual_headlength_cm = ((self.distance_pixels[1] / self.distance_pixels[0]) * self.pixels_to_length_ratio) * (
                            self.distance_pixels[3] / self.distance_pixels[2])
                self.print_to_monitor("Actual headLength: {} cm".format(self.actual_headlength_cm))
                self.actual_bodylength_cm = ((self.distance_pixels[1] / self.distance_pixels[0]) * self.pixels_to_length_ratio) * (
                            self.distance_pixels[4] / self.distance_pixels[2])
                self.print_to_monitor("Actual bodyLength: {} cm".format(self.actual_bodylength_cm))
            elif len(self.distance_pixels) == 3:
                self.actual_headlength_cm = ((self.distance_pixels[1] / self.distance_pixels[
                    0]) * self.pixels_to_length_ratio)
                self.print_to_monitor("Actual headLength: {} cm".format(self.actual_headlength_cm))
                self.actual_bodylength_cm = ((self.distance_pixels[2] / self.distance_pixels[
                    0]) * self.pixels_to_length_ratio)
                self.print_to_monitor("Actual bodyLength: {} cm".format(self.actual_bodylength_cm))
            elif len(self.distance_pixels) == 2:
                self.actual_headlength_cm = ((self.distance_pixels[1] / self.distance_pixels[
                    0]) * self.pixels_to_length_ratio)
                self.print_to_monitor("Actual Length: {} cm".format(self.actual_headlength_cm))
            else:
                self.print_to_monitor("操作存在问题，请反馈开发者处理！")


    # 关闭窗口
    def StopAll(self):
        if askyesno('Dinosaur Measurement', '确定要退出吗？'):
            self.root.quit()
            self.root.destroy()
            exit()


if __name__ == "__main__":
    root = Tk()
    measure = MeasurementTool(root)
    root.mainloop()

