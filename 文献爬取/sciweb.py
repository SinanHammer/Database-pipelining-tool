import tkinter as tk
import tkinter.ttk as ttk
import webbrowser

class WebPageViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Page Viewer")

        # 创建文本框和按钮
        self.entry_title = ttk.Entry(root, width=50)
        self.entry_title.pack(pady=10)

        self.button_search = ttk.Button(root, text="Search", command=self.search_web_page)
        self.button_search.pack(pady=5)

        # 创建WebView控件
        self.web_view = tk.Frame(root, width=800, height=600)
        self.web_view.pack()

        # 设置默认网址为 Sci-Hub
        self.default_url = "https://sci-hub.se/"

    def search_web_page(self):
        title = self.entry_title.get()
        url = self.default_url + title
        webbrowser.open(url)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebPageViewer(root)
    root.mainloop()
