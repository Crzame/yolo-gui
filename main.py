import tkinter as tk
from tkinter import filedialog, messagebox

class YoloApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO 检测工具")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.center_window(400, 300)

        self.model_path = tk.StringVar()

        # 模型选择区域
        tk.Label(root, text="选择 YOLO 模型 (.pt):").pack(pady=10)
        tk.Button(root, text="选择模型", command=self.select_model).pack()
        self.model_label = tk.Label(root, text="未选择模型", fg="gray")
        self.model_label.pack()

        # 操作按钮
        tk.Label(root, text="检测方式:").pack(pady=15)
        tk.Button(root, text="图片检测", width=20, command=self.image_detect).pack(pady=5)
        tk.Button(root, text="视频检测", width=20, command=self.video_detect).pack(pady=5)
        tk.Button(root, text="实时摄像头检测", width=20, command=self.cam_detect).pack(pady=5)

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def select_model(self):
        path = filedialog.askopenfilename(title="选择模型文件", filetypes=[("PyTorch 模型", "*.pt")])
        if path:
            self.model_path.set(path)
            self.model_label.config(text=path, fg="black")

    def image_detect(self):
        print("点击了 图片检测")
        # TODO: 调用图片检测逻辑

    def video_detect(self):
        print("点击了 视频检测")
        # TODO: 调用视频检测逻辑

    def cam_detect(self):
        print("点击了 摄像头检测")
        # TODO: 调用摄像头检测逻辑


if __name__ == "__main__":
    root = tk.Tk()
    app = YoloApp(root)
    root.mainloop()
