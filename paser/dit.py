from tkinter import filedialog
import threading
import fitz
import tkinter as tk
from pdf2image import convert_from_path
from tkinter import ttk
from PIL import Image, ImageTk
import io


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
        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", mode="determinate")
        self.progress_label = tk.Label(self.window, text="")

        self.file_path = None
        self.extracted_text = ""
        self.extracted_images = []
        self.image_references = []

    def select_pdf_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
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

        self.progress_label["text"] = ""
        self.progress_bar["value"] = 0

    def select_image(self, index):
        # 处理图片选择
        # 在这里实现你想要的功能
        print(f"选择的图片：{index + 1}")

    def run(self):
        self.select_button.pack()
        # self.progress_label.pack()
        self.progress_bar.pack(fill=tk.X)
        self.window.mainloop()


if __name__ == "__main__":
    pdf_viewer = PDFViewer()
    pdf_viewer.run()
