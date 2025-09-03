import cv2

# 输入输出视频路径
input_video = "/Users/bytedance/Downloads/304.mp4"
output_video = "304_boxes.mp4"

# 检测结果数据（秒编号）
detections = [
    {'name': 'rabbit', 'frame': 0, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 1, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 2, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 3, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 4, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 5, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 6, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 7, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 8, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 9, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 10, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 11, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 12, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 13, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 14, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 15, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 16, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 17, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 18, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 19, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 20, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 21, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 22, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 23, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 24, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 25, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 26, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 27, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 28, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 29, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 30, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 31, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 32, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 33, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 34, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 35, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 36, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 37, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 38, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 39, 'box': '320 72 960 648'},
    {'name': 'rabbit', 'frame': 40, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 40, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 41, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 41, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 42, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 42, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 43, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 43, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 44, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 44, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 45, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 45, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 46, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 46, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 47, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 47, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 48, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 48, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 49, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 49, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 50, 'box': '320 72 960 648'},
    {'name': 'flower', 'frame': 50, 'box': '256 540 320 576'},
    {'name': 'rabbit', 'frame': 51, 'box': '320 72 960 648'},
    {'name': 'flower', 'frame': 51, 'box': '256 540 320 576'},
    {'name': 'rabbit', 'frame': 52, 'box': '320 72 960 648'},
    {'name': 'apple', 'frame': 52, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 53, 'box': '320 72 960 648'},
    {'name': 'butterfly', 'frame': 53, 'box': '896 144 1024 216'},
    {'name': 'apple', 'frame': 53, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 54, 'box': '320 72 960 648'},
    {'name': 'butterfly', 'frame': 54, 'box': '896 144 1024 216'},
    {'name': 'apple', 'frame': 54, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 55, 'box': '320 72 960 648'},
    {'name': 'butterfly', 'frame': 55, 'box': '896 144 1024 216'},
    {'name': 'apple', 'frame': 55, 'box': '576 468 640 504'},
    {'name': 'rabbit', 'frame': 56, 'box': '320 72 960 648'},
    {'name': 'tree', 'frame': 56, 'box': '1088 324 1216 468'},
    {'name': 'rabbit', 'frame': 57, 'box': '320 72 960 648'},
    {'name': 'tree', 'frame': 57, 'box': '1088 324 1216 468'},
    {'name': 'rabbit', 'frame': 58, 'box': '320 72 960 648'},
    {'name': 'tree', 'frame': 58, 'box': '1088 324 1216 468'},
    {'name': 'rabbit', 'frame': 59, 'box': '320 72 960 648'},
    {'name': 'tree', 'frame': 59, 'box': '1088 324 1216 468'},
    {'name': 'rabbit', 'frame': 60, 'box': '320 72 960 648'},
    {'name': 'tree', 'frame': 60, 'box': '1088 324 1216 468'},
    {'name': 'rabbit', 'frame': 61, 'box': '320 72 960 648'},
    {'name': 'tree', 'frame': 61, 'box': '1088 324 1216 468'},
    {'name': 'rabbit', 'frame': 62, 'box': '320 72 960 648'},
    {'name': 'tree', 'frame': 62, 'box': '1088 324 1216 468'}
]



# 打开视频
cap = cv2.VideoCapture(input_video)
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# 视频输出
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

# 按秒编号分组
detections_by_second = {}
for det in detections:
    sec = det["frame"]  # 秒编号
    x1, y1, x2, y2 = map(int, det["box"].split())
    if sec not in detections_by_second:
        detections_by_second[sec] = []
    detections_by_second[sec].append((x1, y1, x2, y2, det["name"]))

frame_idx = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 当前帧属于第几秒
    current_sec = frame_idx // fps  # 整除

    if current_sec in detections_by_second:
        for (x1, y1, x2, y2, name) in detections_by_second[current_sec]:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, name, (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (0, 255, 0), 2)

    out.write(frame)
    frame_idx += 1

cap.release()
out.release()
print("✅ 按秒加 bbox 视频完成:", output_video)

