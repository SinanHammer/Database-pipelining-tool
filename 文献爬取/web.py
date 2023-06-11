import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

class WebPageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Page Viewer")

        # 创建文本框和按钮
        self.entry_url = ttk.Entry(root, width=50)
        self.entry_url.pack(pady=10)

        self.button_open = ttk.Button(root, text="Open", command=self.open_web_page)
        self.button_open.pack(pady=5)

        # 创建WebView控件
        self.web_view = tk.Frame(root, width=800, height=600)
        self.web_view.pack()

    def open_web_page(self):
        url = self.entry_url.get()
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebPageViewer(root)
    root.mainloop()
