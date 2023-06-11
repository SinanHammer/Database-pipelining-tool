import re
import fitz
import tkinter as tk
from tkinter import scrolledtext


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    return text


def preprocess_text(text):
    # 使用正则表达式删除表格格式
    cleaned_text = re.sub(r'\n\s*\n', '\n', text)  # 删除多余的空行
    cleaned_text = re.sub(r'\n\s*-\s*\n', '\n', cleaned_text)  # 删除横线
    cleaned_text = re.sub(r'\n\s*\|\s*', '\n', cleaned_text)  # 删除竖线
    cleaned_text = re.sub(r'\n\s*\+\s*\n', '\n', cleaned_text)  # 删除加号
    # 可根据需要添加其他清理步骤

    return cleaned_text


def display_text_in_ui(text):
    root = tk.Tk()
    root.title("PDF 文本内容")
    root.geometry("800x600")

    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12))
    text_area.insert(tk.INSERT, text)
    text_area.pack(fill=tk.BOTH, expand=True)

    root.mainloop()


# 读取指定的 PDF 文件并提取文本内容
pdf_file_path = "恐龙.pdf"
extracted_text = extract_text_from_pdf(pdf_file_path)

# 预处理文本内容，删除无关格式
preprocessed_text = preprocess_text(extracted_text)

# 在 UI 界面上显示预处理后的文本内容
display_text_in_ui(preprocessed_text)
