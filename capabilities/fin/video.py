import os

image_folder = "/Users/bytedance/Documents/docs/04_传统金融/海尔/images"
output_video = "output_video.mp4"
fps = 30  # Frames per second
total_duration = 10  # Total video duration
num_images = 3
image_duration = total_duration / num_images  # Time per image

# FFmpeg command with scaling fix
cmd = f"""
ffmpeg -y -framerate 1/{image_duration} -i '{image_folder}/%03d.jpg' \
-vf "scale=1280:-2,format=yuv420p,fps={fps}" -c:v libx264 -t {total_duration} {output_video}
"""
os.system(cmd)
print(f"Video saved as {output_video}")

