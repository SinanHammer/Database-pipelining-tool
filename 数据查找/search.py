import tkinter as tk
from tkinter import filedialog

class TextSearchGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('文本搜索')

        self.import_button = tk.Button(self.root, text='导入文本', command=self.import_text)
        self.import_button.pack()

        self.search_button = tk.Button(self.root, text='搜索', command=self.search_text)
        self.search_button.pack()

        self.text = tk.Text(self.root)
        self.text.pack()

        self.result_label = tk.Label(self.root, text='搜索结果：')
        self.result_label.pack()

        self.result_text = tk.Text(self.root)
        self.result_text.pack()

        self.search_words = ['early', 'today', 'one', 'dinosaur']

    def import_text(self):
        file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    self.text.delete('1.0', tk.END)  # 清空文本框
                    self.text.insert(tk.END, content)
            except UnicodeDecodeError:
                tk.messagebox.showerror('错误', '无法解码文件，请选择其他文件或更改编码方式。')

    def search_text(self):
        keyword = self.text.get('1.0', tk.END).strip()
        for word in self.search_words:
            if word in keyword:
                self.result_text.insert(tk.END, f'关键词 "{word}" 在文本中出现\n')
                break

    def run(self):
        self.root.mainloop()

# 创建TextSearchGUI对象并运行界面
gui = TextSearchGUI()
gui.run()
