import cv2
import os

def video_to_images(video_path, output_folder, frame_interval=30):
    """
    Extracts images from a video at regular intervals.

    :param video_path: Path to the video file.
    :param output_folder: Folder where images will be saved.
    :param frame_interval: Interval between frames to be saved (in frames).
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Load the video
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Unable to open video.")
        return
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps
    
    print(f"Video Duration: {duration:.2f} seconds, FPS: {fps}, Total Frames: {frame_count}")
    
    frame_index = 0
    saved_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Save every `frame_interval`-th frame
        if frame_index % frame_interval == 0:
            image_path = os.path.join(output_folder, f"frame_{frame_index:06d}.jpg")
            cv2.imwrite(image_path, frame)
            saved_count += 1
        
        frame_index += 1
    
    cap.release()
    print(f"Finished. {saved_count} images saved to {output_folder}.")

# Example usage:
video_path = "/Users/bytedance/Downloads/sample_vedio.mp4"  # Replace with your MP4 file path
output_folder = "/Users/bytedance/Downloads/output_images"  # Folder to save images
frame_interval = 60  # Save an image every 60 frames

video_to_images(video_path, output_folder, frame_interval)

