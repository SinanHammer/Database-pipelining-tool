import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext


class DataProcessorGUI(object):
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("数据库处理程序")
        self.window.geometry("500x300")
        self.create_widgets()

    def create_widgets(self):
        # 创建文本框和选择按钮的容器框架
        self.frame_data1 = tk.Frame(self.window)
        self.frame_data1.pack(side=tk.TOP, pady=10)

        self.frame_data2 = tk.Frame(self.window)
        self.frame_data2.pack(side=tk.TOP, pady=10)

        self.frame_output_path = tk.Frame(self.window)
        self.frame_output_path.pack(side=tk.TOP, pady=10)

        # 创建监测窗口
        self.monitor_window = scrolledtext.ScrolledText(self.window, height=5, width=50)
        self.monitor_window.pack(side=tk.TOP, padx=10, pady=10)

        # 创建文本框和选择按钮
        self.label_data1 = tk.Label(self.frame_data1, text="导入数据1：")
        self.label_data1.pack(side=tk.LEFT)

        self.text_data1 = tk.Text(self.frame_data1, height=1.5, width=30)
        self.text_data1.pack(side=tk.LEFT)

        self.btn_import_data1 = tk.Button(self.frame_data1, text="选择文件", command=self.import_data1)
        self.btn_import_data1.pack(side=tk.RIGHT)

        self.label_data2 = tk.Label(self.frame_data2, text="导入数据2：")
        self.label_data2.pack(side=tk.LEFT)

        self.text_data2 = tk.Text(self.frame_data2, height=1.5, width=30)
        self.text_data2.pack(side=tk.LEFT)

        self.btn_import_data2 = tk.Button(self.frame_data2, text="选择文件", command=self.import_data2)
        self.btn_import_data2.pack(side=tk.RIGHT)

        self.label_output_path = tk.Label(self.frame_output_path, text="生成路径：")
        self.label_output_path.pack(side=tk.LEFT)

        self.text_output_path = tk.Text(self.frame_output_path, height=1.5, width=30)
        self.text_output_path.pack(side=tk.LEFT)

        self.btn_select_output_path = tk.Button(self.frame_output_path, text="选择路径", command=self.select_output_path)
        self.btn_select_output_path.pack(side=tk.RIGHT)

        # 创建运行按钮
        self.btn_run = tk.Button(self.window, text="运行", command=self.generate_result)
        self.btn_run.pack(side=tk.BOTTOM, pady=20)

    def import_data1(self):
        file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
        self.text_data1.delete('1.0', tk.END)
        self.text_data1.insert(tk.END, file_path)
        print("数据1导入成功。")

    def import_data2(self):
        file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
        self.text_data2.delete('1.0', tk.END)
        self.text_data2.insert(tk.END, file_path)
        print("数据2导入成功。")

    def select_output_path(self):
        folder_path = filedialog.askdirectory()
        self.text_output_path.delete('1.0', tk.END)
        self.text_output_path.insert(tk.END, folder_path)
        print("生成文件路径已选择：", folder_path)

    def generate_result(self):
        data1_path = self.text_data1.get('1.0', tk.END).strip()
        data2_path = self.text_data2.get('1.0', tk.END).strip()
        output_path = self.text_output_path.get('1.0', tk.END).strip()

        if data1_path and data2_path and output_path:
            # 使用选定的文件路径导入数据1和数据2
            data1 = pd.read_excel(data1_path)
            data2 = pd.read_excel(data2_path)

            # 执行数据处理逻辑，生成结果
            # 构建最终结果
            result_data = []

            for i in range(len(data1)):
                d1 = data1.iloc[i]
                d2 = data2[data2['reference_no'] == d1['reference_no']]
                row_data = {
                    'Group': 'Tetrapod',
                    'Guild': '',
                    'Taxon': d1['accepted_name'],
                    'Location': (str(d1['state']) + 'State,' if d1['state'] else '') + (
                        str(d1['cc']) if d1['cc'] else ''),
                    'Foamation': d1['formation'],
                    'Age': str(d1['early_interval']) + '-' + str(d1['late_interval']),
                    'Length of Skull (头骨长度, mm）': '',
                    'Length of whole body （身体长度,cm）': '',
                    'Reference': str(d2['author1last'].values[0]) + ' ' + 'et al.' + str(
                        d2['pubyr'].values[0]) + "." + str(d2['reftitle'].values[0]) if d2['doi'].isnull().values[
                        0] else str(d2['author1last'].values[0]) + ' ' + 'et al.' + str(
                        d2['pubyr'].values[0]) + '.' + str(d2['pubtitle'].values[0]),
                    'DOI': d2['doi'],
                    'title': d2['reftitle']
                }
                row_df = pd.DataFrame(row_data)
                result_data.append(row_df)

            result = pd.concat(result_data, ignore_index=True)
            output_path = output_path + "\恐龙数据库.xlsx"
            result.to_excel(output_path)
            result.clear()
            # 输出运行状态到监测窗口
            self.monitor_window.insert(tk.END, "代码运行成功！\n")
            self.monitor_window.insert(tk.END, f"保存地址为：{output_path}")

        else:
            self.monitor_window.insert(tk.END, "请先选择数据文件和生成文件路径。\n")

    def run(self):
        # 开始UI事件循环
        self.window.mainloop()

