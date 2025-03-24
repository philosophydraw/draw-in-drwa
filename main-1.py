import cv2
import os
import sys
import re
import numpy as np
from PIL import Image


def create_video_from_images(image_folder, output_folder, output_name='output.mp4', fps=30):
    # 统一处理路径格式（解决中文路径问题）
    image_folder = os.path.normpath(image_folder).replace("\\", "/")
    output_folder = os.path.normpath(output_folder).replace("\\", "/")

    # 验证输入文件夹
    if not os.path.exists(image_folder):
        print(f"错误: 输入文件夹 '{image_folder}' 不存在")
        return

    # 自动创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 获取并排序图片文件
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
    image_files = []

    try:
        # 自然排序函数
        def natural_sort_key(s):
            return [int(c) if c.isdigit() else c.lower() for c in re.split(r'(\d+)', s)]

        # 遍历并筛选文件
        for filename in sorted(os.listdir(image_folder), key=natural_sort_key):
            filepath = os.path.join(image_folder, filename).replace("\\", "/")

            # 跳过子目录和非文件对象
            if not os.path.isfile(filepath):
                print(f"跳过非文件对象: {filepath}")
                continue

            # 验证文件扩展名
            _, ext = os.path.splitext(filename)
            if ext.lower() in valid_extensions:
                image_files.append(filepath)
    except Exception as e:
        print(f"读取文件夹失败: {e}")
        return

    # 检查有效文件
    if not image_files:
        print("错误: 未找到任何有效图片文件")
        return

    # 获取视频尺寸（使用PIL提高兼容性）
    try:
        with Image.open(image_files[0]) as img:
            width, height = img.size
    except Exception as e:
        print(f"无法读取首帧图片: {e}")
        return

    # 创建视频写入器
    output_path = os.path.join(output_folder, output_name).replace("\\", "/")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not video.isOpened():
        print("错误: 无法创建视频文件，请检查编码器")
        return

    # 处理图片
    total = len(image_files)
    for idx, img_path in enumerate(image_files, 1):
        try:
            # 使用PIL读取解决OpenCV兼容性问题
            pil_img = Image.open(img_path).convert('RGB')
            frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(f"警告: 跳过损坏文件 [{os.path.basename(img_path)}] - {e}")
            continue

        video.write(frame)
        print(f"进度: {idx}/{total} ({idx / total:.1%}) - {os.path.basename(img_path)}")

    # 释放资源
    video.release()
    print(f"\n视频已生成: {output_path}")


if __name__ == "__main__":
    # 默认路径（原始字符串处理Windows路径）
    input_folder = r"D:\桌面\课程学习\8-编程语言\4-python\图片转视频\input\test"
    output_folder = r"D:\桌面\课程学习\8-编程语言\4-python\图片转视频\output"
    output_name = "output.mp4"
    fps = 4

    # 命令行参数处理
    if len(sys.argv) >= 3:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
    elif len(sys.argv) == 2:
        input_folder = sys.argv[1]

    print(f"正在转换: {input_folder} → {output_folder}")

    create_video_from_images(
        image_folder=input_folder,
        output_folder=output_folder,
        output_name=output_name,
        fps=fps
    )