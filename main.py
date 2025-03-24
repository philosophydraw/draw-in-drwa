import cv2
import os
import sys

def create_video_from_images(image_folder, output_folder, output_name='output.mp4', fps=30, target_size=(640, 480)):
    # 检查输入文件夹是否存在
    if not os.path.exists(image_folder):
        print(f"错误: 输入文件夹 '{image_folder}' 不存在。")
        return
    
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"已创建输出文件夹: {output_folder}")
    
    # 获取所有JPG图片文件
    image_files = []
    valid_extension = '.jpg'  # 只处理JPG格式的图片
    
    try:
        for file in sorted(os.listdir(image_folder)):
            ext = os.path.splitext(file)[1].lower()
            if ext == valid_extension:
                image_file_path = os.path.join(image_folder, file)
                # 检查文件是否存在且可读取
                if os.path.isfile(image_file_path) and os.access(image_file_path, os.R_OK):
                    image_files.append(image_file_path)
                else:
                    print(f"警告: 文件存在性问题或权限不足，将跳过此文件: {image_file_path}")
    
    except Exception as e:
        print(f"读取文件夹内容时发生错误: {e}")
        return
    
    if not image_files:
        print(f"在 {image_folder} 文件夹中没有找到可读取的JPG图片文件")
        return
    
    # 设置视频写入器，使用目标大小作为视频尺寸
    output_path = os.path.join(output_folder, output_name)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, target_size)
    
    # 处理每一张图片，统一大小后写入视频
    total_images = len(image_files)
    for idx, image_file in enumerate(image_files, 1):
        frame = cv2.imread(image_file)
        if frame is not None:
            # 调整图片大小
            resized_frame = cv2.resize(frame, target_size)
            video.write(resized_frame)
            print(f"处理进度: {idx}/{total_images} - {image_file}")
        else:
            print(f"警告: 无法读取图片（尽管之前检查通过），将跳过此文件: {image_file}")
    
    # 释放资源
    video.release()
    print(f"\n视频已保存到: {output_path}")

if __name__ == "__main__":
    # 默认参数（如果命令行没有提供）
    input_folder = 'D:\\桌面\\课程学习\\8-编程语言\\4-python\\图片转视频\\input\\test'
    output_folder = 'D:\\桌面\\课程学习\\8-编程语言\\4-python\\图片转视频\\output'
    output_name = 'output.mp4'
    fps = 30
    target_size = (640, 480)  # 目标图片大小，例如640x480
    
    # 命令行参数处理
    if len(sys.argv) >= 4:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        target_size = tuple(map(int, sys.argv[3].split(',')))  # 从命令行获取目标大小，例如"640,480"
    elif len(sys.argv) == 3:
        input_folder = sys.argv[1]
        output_folder = sys.argv[2]
        print("警告: 未指定图片目标大小，将使用默认大小。")
    elif len(sys.argv) == 2:
        input_folder = sys.argv[1]
        print("警告: 未指定输出文件夹和图片目标大小，将使用默认设置。")
    
    print(f"准备将 '{input_folder}' 文件夹中的JPG图片转换为视频，目标大小为 {target_size}...")
    
    # 调用函数，将指定文件夹中的图片转换为视频
    create_video_from_images(
        image_folder=input_folder,
        output_folder=output_folder,
        output_name=output_name,
        fps=fps,
        target_size=target_size
    )