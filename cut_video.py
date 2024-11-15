import ffmpeg


def trim_video(input_path, output_path, start_frame, end_frame, fps=30):
    # 根据FPS计算开始时间和结束时间（秒数）
    start_time = start_frame / fps
    duration = (end_frame - start_frame) / fps

    # 使用ffmpeg进行视频裁剪
    (
        ffmpeg
        .input(input_path, ss=start_time, t=duration)  # 设置开始时间和裁剪时长
        .output(output_path, vcodec='mpeg4')  # 设置编码器和质量参数
        .run()
    )


# 示例使用
input_path = r"D:\华毅\目标追踪数据集\1_艾维\20240113-104949_rack-5_right_RGB.mp4"  # 输入视频路径
output_path = r"D:\华毅\目标追踪数据集\test\aiwei_2_cut.mp4"  # 输出视频路径
start_frame = 350  # 起始帧
end_frame = 410  # 结束帧
fps = 30  # 视频帧率 (请根据实际帧率设置)

trim_video(input_path, output_path, start_frame, end_frame, fps)
