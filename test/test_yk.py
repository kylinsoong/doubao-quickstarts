import tkinter as tk
from tkinter import filedialog

# 创建主窗口
root = tk.Tk()
root.title("文件上传至TOS")
root.geometry("400x200")

# 用于存储选择的文件路径
file_path = tk.StringVar()
file_path.set("请选择文件")

# 创建标签显示文件路径
file_label = tk.Label(root, textvariable=file_path)
file_label.pack(pady=20)

# 选择文件的函数
def select_file():
    path = filedialog.askopenfilename()
    if path:
        file_path.set(path)

# 选择文件按钮
select_button = tk.Button(root, text="选择文件", command=select_file)
select_button.pack()

# 上传文件的函数
def upload_file():
    path = file_path.get()
    if path != "请选择文件":
        print(path)
        try:
            # 替换为你的Bucket名称
            bucket_name = "your-bucket-name"
            # 获取文件名
            object_key = path.split("/")[-1]
            # 上传文件到TOS
        except Exception as e:
            print(f"上传过程中出现错误: {e}")
    else:
        print("请先选择文件")

# 上传文件按钮
upload_button = tk.Button(root, text="上传文件", command=upload_file)
upload_button.pack()

# 运行主循环
root.mainloop()
