import subprocess

def run_yolo_detection(model_path, image_path, output_dir='runs/detect'):
    """
    调用 YOLOv5 的 detect.py 进行图片检测
    """
    command = [
        'python', '../yolov5/detect.py',
        '--weights', model_path,
        '--source', image_path,
        '--conf', '0.25',
        '--save-txt',
        '--save-conf',
        '--project', output_dir,
        '--exist-ok'  # 如果目标文件夹已存在就复用
    ]

    try:
        subprocess.run(command, check=True)
        print("✅ 检测完成！结果保存在:", output_dir)
    except subprocess.CalledProcessError as e:
        print("❌ 检测失败:", e)

# 示例用法
run_yolo_detection(
    model_path='yolov5s.pt',          # 你的模型路径
    image_path='cat.jpg'  # 你的图片路径
)