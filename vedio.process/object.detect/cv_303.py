import cv2

# 输入输出视频路径
input_video = "/Users/bytedance/Downloads/303.mp4"
output_video = "output_with_boxes.mp4"

# 检测结果数据（秒编号）
detections = [
  {"name": "Switch", "frame": 0, "box": "38 108 52 116"},
  {"name": "Rack", "frame": 0, "box": "374 27 432 40"},
  {"name": "Door", "frame": 0, "box": "264 13 336 162"},
  {"name": "Chair", "frame": 0, "box": "182 102 216 156"},
  {"name": "Table", "frame": 0, "box": "201 129 249 156"},
  {"name": "Blinds", "frame": 0, "box": "105 48 240 129"},
  {"name": "Person", "frame": 2, "box": "249 81 302 162"},
  {"name": "Person", "frame": 3, "box": "216 75 278 162"},
  {"name": "Person", "frame": 4, "box": "192 75 264 162"},
  {"name": "Person", "frame": 5, "box": "168 81 249 189"},
  {"name": "Person", "frame": 6, "box": "120 94 230 202"},
  {"name": "Person", "frame": 7, "box": "105 94 216 202"},
  {"name": "Person", "frame": 8, "box": "96 94 206 202"},
  {"name": "Computer", "frame": 4, "box": "38 148 96 175"},
  {"name": "Computer Desk", "frame": 4, "box": "144 162 312 202"},
  {"name": "Speaker", "frame": 4, "box": "115 121 139 140"},
  {"name": "Decoration", "frame": 4, "box": "67 102 163 129"},
  {"name": "Bookshelf", "frame": 4, "box": "0 121 33 175"},
  {"name": "Chair", "frame": 4, "box": "19 156 115 202"}
]


backup = [
    {'name': '开关', 'frame': 0, 'box': '38 108 52 116'},
    {'name': '架子', 'frame': 0, 'box': '374 27 432 40'},
    {'name': '门', 'frame': 0, 'box': '264 13 336 162'},
    {'name': '椅子', 'frame': 0, 'box': '182 102 216 156'},
    {'name': '桌子', 'frame': 0, 'box': '201 129 249 156'},
    {'name': '百叶窗', 'frame': 0, 'box': '105 48 240 129'},
    {'name': '人', 'frame': 2, 'box': '249 81 302 162'},
    {'name': '人', 'frame': 3, 'box': '216 75 278 162'},
    {'name': '人', 'frame': 4, 'box': '192 75 264 162'},
    {'name': '人', 'frame': 5, 'box': '168 81 249 189'},
    {'name': '人', 'frame': 6, 'box': '120 94 230 202'},
    {'name': '人', 'frame': 7, 'box': '105 94 216 202'},
    {'name': '人', 'frame': 8, 'box': '96 94 206 202'},
    {'name': '电脑', 'frame': 4, 'box': '38 148 96 175'},
    {'name': '电脑桌', 'frame': 4, 'box': '144 162 312 202'},
    {'name': '扬声器', 'frame': 4, 'box': '115 121 139 140'},
    {'name': '装饰品', 'frame': 4, 'box': '67 102 163 129'},
    {'name': '书架', 'frame': 4, 'box': '0 121 33 175'},
    {'name': '椅子', 'frame': 4, 'box': '19 156 115 202'}
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

