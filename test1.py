import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import subprocess
import os


class Config:
    MODEL_DIR = "./models"
    ICON_DIR = "./icons"
    IMAGE_DIR = "./images"
    RESULT_DIR = "runs/detect/exp"
    YOLO_DETECT_SCRIPT = "../yolov5/detect.py"


class YoloUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLO 检测工具")
        # self.root.geometry("1200x600")
        self.root.resizable(False, False)
        # 设置大小并居中
        self.center_window(1200, 600)

        # ========== 主结构：左边操作区 + 右边显示区 ==========
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧：操作区域
        self.left_frame = tk.Frame(self.main_frame, width=300, padx=10, pady=10, bg='pink')
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # 右侧：显示区域
        self.right_frame = tk.Frame(self.main_frame, bg="lightgray")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.load_models()
        self.setup_left_controls()
        self.setup_right_view()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def load_models(self):
        # ========== 模型名列表

        self.model_list = [f for f in os.listdir(Config.MODEL_DIR) if f.endswith(".pt")]
        # ========== 模型路径映射表
        self.model_paths = {f: os.path.join(Config.MODEL_DIR, f) for f in self.model_list}

    def on_model_selected(self, event=None):
        selected_name = self.model_combobox.get()
        self.model_path = self.model_paths.get(selected_name)

    def setup_left_controls(self):
        # 模型选择按钮
        tk.Label(self.left_frame, text="选择 YOLO 模型:").pack(pady=5)

        # self.model_combobox = ttk.Combobox(self.left_frame, values=self.model_list, state="readonly")
        # self.model_combobox.pack(pady=5)
        # self.model_combobox.bind("<<ComboboxSelected>>", self.on_model_selected)
        #
        # icon_path = os.path.join(Config.ICON_DIR, "model.png")
        # try:
        #     icon_image = Image.open(icon_path)
        #     icon_image = icon_image.resize((24, 24), Image.ANTIALIAS)
        #     self.icon_photo = ImageTk.PhotoImage(icon_image)
        #     tk.Button(self.left_frame, image=self.icon_photo, command=self.select_model_from_anywhere).pack(pady=5)
        # except Exception as e:
        #     print(f"加载图标失败: {e}")
        #     tk.Button(self.left_frame, text="浏览模型文件", command=self.select_model_from_anywhere).pack(pady=5)
        model_row = tk.Frame(self.left_frame)
        model_row.pack(pady=5)

        self.model_combobox = ttk.Combobox(model_row, values=self.model_list, state="readonly", width=22)
        self.model_combobox.grid(row=0, column=0, padx=5)
        self.model_combobox.bind("<<ComboboxSelected>>", self.on_model_selected)

        icon_path = os.path.join(Config.ICON_DIR, "model.png")
        try:
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((24, 24), Image.ANTIALIAS)
            self.icon_photo = ImageTk.PhotoImage(icon_image)
            # 改为普通图片展示，而不是按钮
            icon_label = tk.Label(model_row, image=self.icon_photo, cursor="hand2")
            icon_label.grid(row=0, column=1)
            # 绑定点击事件
            icon_label.bind("<Button-1>", lambda event: self.select_model_from_anywhere())
        except Exception as e:
            print(f"加载图标失败: {e}")
            tk.Button(model_row, text="浏览模型文件", command=self.select_model_from_anywhere).grid(row=0, column=1)

        tk.Button(self.left_frame, text='上传图片', command=self.upload_image).pack(pady=5)
        # 操作按钮
        tk.Label(self.left_frame, text="检测模式:").pack(pady=15)
        tk.Button(self.left_frame, text="图片检测", command=self.image_detect, width=20).pack(pady=5)
        tk.Button(self.left_frame, text="视频检测", command=self.video_detect, width=20).pack(pady=5)
        tk.Button(self.left_frame, text="实时摄像头检测", command=self.cam_detect, width=20).pack(pady=5)

    def setup_right_view(self):
        # 创建两个Label用于显示原图与检测结果
        self.original_label = tk.Label(self.right_frame, text="原图/视频", bg="blue")
        self.original_label.place(x=10, y=120, width=480, height=360)  # 明确像素大小

        self.result_label = tk.Label(self.right_frame, text="检测结果", bg="white")
        self.result_label.place(x=500, y=120, width=480, height=360)


    def select_model_from_anywhere(self):
        file_path = filedialog.askopenfilename(
            title="选择 YOLOv5 模型文件",
            filetypes=[("PyTorch 模型", "*.pt")]
        )
        if file_path:
            filename = os.path.basename(file_path)

            # 如果是新模型，添加进下拉框
            if filename not in self.model_list:
                self.model_list.append(filename)
                self.model_paths[filename] = file_path
                self.model_combobox["values"] = self.model_list

            # 设置当前选择项
            self.model_combobox.set(filename)
            self.model_path = file_path

            messagebox.showinfo("模型选择成功", f"已选择模型文件:\n{file_path}")

    def show_image_to_label(self, image_path, label_widget):
        """将图片按比例缩放后，显示到指定的 Label 中（不超出、不变形）"""
        try:
            # 1. 打开图片
            image = Image.open(image_path)

            # 2. 获取 label 大小
            label_width = label_widget.winfo_width()
            label_height = label_widget.winfo_height()

            # 如果第一次执行时，label 还没有尺寸，先手动设置默认值
            if label_width == 1 or label_height == 1:
                label_width = 480
                label_height = 360

            # 3. 计算等比例缩放后的大小
            image_ratio = image.width / image.height
            label_ratio = label_width / label_height

            if image_ratio > label_ratio:
                # 图片太宽
                new_width = label_width
                new_height = int(label_width / image_ratio)
            else:
                # 图片太高
                new_height = label_height
                new_width = int(label_height * image_ratio)

            # 4. 缩放图片
            resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized_image)

            # 5. 显示图片
            label_widget.config(image=photo)
            label_widget.image = photo  # 防止垃圾回收
        except Exception as e:
            print(f"加载图片失败: {e}")

    def upload_image(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.show_image_to_label(file_path, self.original_label)

    def image_detect(self):
        if not hasattr(self, "model_path") or not hasattr(self, "image_path"):
            messagebox.showwarning("缺少信息", "请先选择模型并上传图片")
            return

        try:
            result_dir = 'runs/detect/exp'
            cmd = [
                'python', '../yolov5/detect.py',
                '--weights', self.model_path,
                '--source', self.image_path,
                '--conf', '0.25',
                '--save-txt',
                '--save-conf',
                '--project', 'runs/detect',
                '--exist-ok'
            ]
            subprocess.run(cmd, check=True)

            # 检测完显示右边图片
            import os
            img_name = os.path.basename(self.image_path)
            result_path = os.path.join(result_dir, img_name)
            if os.path.exists(result_path):
                self.show_image_to_label(result_path, self.result_label)
            else:
                messagebox.showerror("失败", "检测结果图未找到")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("检测错误", f"检测失败：\n{e}")

    def video_detect(self):
        print("点击了 视频检测")
        # TODO: 加载视频帧截图并显示

    def cam_detect(self):
        print("点击了 实时摄像头检测")
        # TODO: 实时摄像头读取与展示


if __name__ == "__main__":
    root = tk.Tk()
    app = YoloUI(root)
    root.mainloop()
