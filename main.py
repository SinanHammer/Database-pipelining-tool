import tkinter as tk
from tkinter import messagebox
from data_processing.treat_data_ui import DataProcessorGUI
from picture_distance_measurement.Dinosaur_Measurement_1 import MeasurementTool as M
# from image_text.image_text_separation import PDFViewer
from tkinter import filedialog
import threading
import fitz
import tkinter as tk
from pdf2image import convert_from_path
from tkinter import ttk
from PIL import Image, ImageTk
import io
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import fitz
import io
import os
import threading
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import fitz
import io
import os


class PDFViewer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("PDF Viewer")

        self.text_frame = tk.Frame(self.window)
        self.text_scrollbar = tk.Scrollbar(self.text_frame)
        self.text_area = tk.Text(self.text_frame, height=10, width=50, yscrollcommand=self.text_scrollbar.set)
        self.text_scrollbar.config(command=self.text_area.yview)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas_frame = tk.Frame(self.window)
        self.canvas_scrollbar = tk.Scrollbar(self.canvas_frame)
        self.canvas = tk.Canvas(self.canvas_frame, width=400, height=400, yscrollcommand=self.canvas_scrollbar.set)
        self.canvas_scrollbar.config(command=self.canvas.yview)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.select_button = tk.Button(self.window, text="选择PDF", command=self.select_pdf_file)

        self.input_text = tk.Text(self.window, width=15, height=1.5)
        self.input_text.pack()

        self.select_save_button = tk.Button(self.window, text="选择保存位置", command=self.select_save_location)
        self.select_save_button.pack()

        self.Text = tk.Text(self.window, width=15, height=1.5)
        self.Text.pack()

        self.generate_button = tk.Button(self.window, text="生成文本", command=self.generate_text_file)
        self.generate_button.pack()

        self.output_text = tk.Text(self.window, height=15, width=15)
        self.output_text.pack(side=tk.BOTTOM)

        self.file_path = None
        self.extracted_text = ""
        self.extracted_images = []
        self.image_references = []
        self.photo_references = []  # 存储PhotoImage对象的引用
        self.save_location = ""
        self.image_path = ""

    def select_pdf_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        print("选择的文件地址是：", self.file_path)
        self.output_text.insert(tk.END, str("选择的文件地址是：" + self.file_path))
        if self.file_path:
            extraction_thread = threading.Thread(target=self.extract_and_display)
            extraction_thread.start()

    def extract_and_display(self):
        self.extract_text_and_images_from_pdf()
        self.window.after(0, self.display_text_and_images_in_ui)

    def extract_text_and_images_from_pdf(self):
        doc = fitz.open(self.file_path)
        text = ""
        images = []
        for page in doc:
            text += page.get_text("text")
            for image in page.get_images():
                xref = image[0]
                base_image = doc.extract_image(xref)
                image_data = base_image["image"]
                image_mode = base_image["colorspace"]
                if image_mode == 8:
                    image_mode = "RGB"
                image_data = bytes(image_data)
                pil_image = Image.open(io.BytesIO(image_data))
                if image_mode == 4:
                    pil_image = pil_image.convert("RGB")
                images.append(pil_image)
        self.extracted_text = text
        self.extracted_images = images

    def display_text_and_images_in_ui(self):
        self.text_area.configure(state='normal')
        self.text_area.delete('1.0', tk.END)
        self.text_area.insert(tk.END, self.extracted_text)
        self.text_area.configure(state='disabled')

        self.canvas.delete("all")
        self.image_references = []
        self.photo_references = []  # 清空PhotoImage对象的引用列表

        y = 0
        button_offset = 20  # 按钮的垂直偏移量
        for index, image in enumerate(self.extracted_images):
            # 调整图片尺寸
            width, height = image.size
            max_width = self.canvas.winfo_width()  # 获取画布的宽度
            if width > max_width:
                scaled_height = int(height * max_width / width)
                image = image.resize((max_width, scaled_height), Image.ANTIALIAS)
                height = scaled_height

            photo = ImageTk.PhotoImage(image)
            self.image_references.append(photo)
            self.photo_references.append(photo)  # 存储PhotoImage对象的引用

            self.canvas.create_image(max_width // 2, y + height // 2, image=photo, anchor=tk.CENTER)

            # 创建图片选择按钮
            button = tk.Button(self.canvas, text=f"选择图片 {index + 1}", command=lambda idx=index: self.select_image(idx))
            button_window = self.canvas.create_window(max_width // 2, y - button_offset, window=button,
                                                      anchor=tk.CENTER)
            # 更新按钮位置
            self.canvas.update()
            bbox = self.canvas.bbox(button_window)
            y += bbox[3] - bbox[1] + button_offset

            y += height

        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def select_image(self, index):
        # 处理图片选择
        if index < len(self.photo_references):
            selected_image = self.extracted_images[index]
            save_path = os.path.join(self.save_location, f"image_{index + 1}.jpg")
            self.image_path = save_path
            selected_image.save(save_path)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "图片保存路径: " + save_path + "\n")
        else:
            print("无效的图片索引")
            self.output_text.insert(tk.END, "无效的图片索引\n")

    def generate_text_file(self):
        text = self.Text.get("1.0", tk.END).strip()  # 获取文本框中的内容
        if text and self.save_location:
            file_path = os.path.join(self.save_location, f"{text}.txt")
            with open(file_path, "w", encoding="utf-8") as file:  # 使用utf-8编码保存文本
                file.write(self.extracted_text)
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, f"成功创建文本 {text}.txt!\n")
        else:
            self.output_text.delete('1.0', tk.END)
            self.output_text.insert(tk.END, "请先选择保存位置和输入文本")

    def select_save_location(self):
        save_location = filedialog.askdirectory()
        self.input_text.delete("1.0", tk.END)  # 清空文本框内容
        self.input_text.insert(tk.END, save_location)  # 在文本框中插入保存位置
        if save_location:
            self.save_location = save_location
            print("选择的文件保存地址是：{}".format(self.save_location))
            self.output_text.insert(tk.END, "选择的文件保存地址是：{}".format(self.save_location))

    def run(self):
        self.select_button.pack()
        self.window.mainloop()


class Application(PDFViewer):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("论文数据处理工具")
        self.create_menu_buttons()

    def create_menu_buttons(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack()

        menus = ["数据处理", "图像处理", "属性查询"]
        for menu in menus:
            menu_button = tk.Button(menu_frame, text=menu, command=lambda m=menu: self.menu_click(m))
            menu_button.pack(side="left", padx=10, pady=10)

    def menu_click(self, menu):
        if menu == "数据处理":
            self.data_processing_window()
        elif menu == "图像处理":
            self.image_processing_window()
        elif menu == "属性查询":
            self.attribute_query_window()

    def data_processing_window(self):
        data_processor_gui = DataProcessorGUI()
        data_processor_gui.run()

    def image_processing_window(self):
        image_processing_gui = M()
        image_processing_gui.run()

    def attribute_query_window(self):
        pdf_viewer = PDFViewer()
        pdf_viewer.run()

    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    app = Application()
    app.run()
