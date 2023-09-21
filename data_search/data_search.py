import tkinter as tk
from tkinter import filedialog


class TextSearchGUI(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('文本搜索')

        self.import_button = tk.Button(self.root, text='导入文本', command=self.import_text)
        self.import_button.pack(side=tk.RIGHT)

        self.search_button = tk.Button(self.root, text='搜索', command=self.search_text)
        self.search_button.pack(side=tk.RIGHT)

        self.confirm_button = tk.Button(self.root, text='确认', command=self.confirm_selection, state=tk.DISABLED)
        self.confirm_button.pack(side=tk.RIGHT)

        self.text = tk.Text(self.root)
        self.text.pack(side=tk.LEFT, padx=10)

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(side=tk.RIGHT, padx=10)

        self.result_label = tk.Label(self.result_frame, text='搜索结果：')
        self.result_label.pack()

        self.result_checkbuttons = []
        self.search_words = ['early', '今天', '一个', '恐龙']

        self.highlight_start = '1.0'
        self.highlight_end = '1.0'

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
        self.clear_result_checkbuttons()
        self.remove_highlight()

        found_results = {}
        for word in self.search_words:
            count = keyword.count(word)
            if count > 0:
                found_results[word] = count

        if found_results:
            self.result_label.configure(text='搜索结果：')
            for word, count in found_results.items():
                var = tk.BooleanVar()
                checkbutton = tk.Checkbutton(self.result_frame, text=word, variable=var)
                checkbutton.pack(anchor=tk.W)
                checkbutton.bind('<Button-1>', lambda event, w=word: self.highlight_word(w))
                checkbutton.config(command=self.update_confirm_button_state)
                self.result_checkbuttons.append((checkbutton, var))
                count_label = tk.Label(self.result_frame, text=f'出现次数：{count}')
                count_label.pack(anchor=tk.W)
        else:
            self.result_label.configure(text='搜索结果：无匹配项')

    def clear_result_checkbuttons(self):
        for checkbutton, var in self.result_checkbuttons:
            checkbutton.pack_forget()
            checkbutton.destroy()
        self.result_checkbuttons.clear()

    def highlight_word(self, word):
        self.remove_highlight()
        start_index = '1.0'
        while True:
            start_index = self.text.search(word, start_index, stopindex=tk.END)
            if not start_index:
                break
            end_index = f'{start_index}+{len(word)}c'
            self.text.tag_add('highlight', start_index, end_index)
            start_index = end_index
        self.text.tag_config('highlight', background='yellow')
        self.text.tag_raise('highlight')
        self.highlight_start = '1.0'
        self.highlight_end = start_index

    def remove_highlight(self):
        self.text.tag_remove('highlight', '1.0', tk.END)

    def update_confirm_button_state(self):
        selected_results = [checkbutton[1].get() for checkbutton in self.result_checkbuttons]
        if any(selected_results):
            self.confirm_button.config(state=tk.NORMAL)
        else:
            self.confirm_button.config(state=tk.DISABLED)

    def confirm_selection(self):
        selected_results = [checkbutton[0].cget('text') for checkbutton in self.result_checkbuttons if checkbutton[1].get()]
        for result in selected_results:
            print(result)

    def run(self):
        self.root.mainloop()


# 创建TextSearchGUI对象并运行界面
gui = TextSearchGUI()
gui.run()
