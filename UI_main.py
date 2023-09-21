import tkinter as tk
from tkinter import messagebox
from data_processing.treat_data_ui import DataProcessorGUI
from picture_distance_measurement.Dinosaur_Measurement_1 import MeasurementTool as M
from paser.image_text_separation import PDFViewer

def data_processing_window():
    # 创建数据处理窗口
    data_processor_gui = DataProcessorGUI()
    data_processor_gui.run()


def image_processing_window(image_path):
    image_processing_gui = M()
    if image_path:
        image_processing_gui.image_path = image_path
    image_processing_gui.run()

def attribute_query_window():
    # 创建属性查询窗口
    pdf_viewer = PDFViewer()
    pdf_viewer.run()
    # if pdf_viewer.image_path:
    #     image_processing_window(pdf_viewer.image_path)
    # else:
    #     pass


# 创建主窗口
root = tk.Tk()
root.title("恐龙数据库处理工具")

# 菜单点击事件处理函数
def menu_click(menu):
    if menu == "数据处理":
        data_processing_window()
    elif menu == "图像处理":
        image_processing_window()
    elif menu == "属性查询":
        attribute_query_window()

# 创建菜单按钮
menu_frame = tk.Frame(root)
menu_frame.pack()

menus = ["数据处理", "图像处理", "属性查询"]
for menu in menus:
    menu_button = tk.Button(menu_frame, text=menu, command=lambda m=menu: menu_click(m))
    menu_button.pack(side="left", padx=10, pady=10)

# 运行主循环
root.mainloop()
