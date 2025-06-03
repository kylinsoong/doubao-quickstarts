import os
import tos
import time
import logging
from moviepy.editor import VideoFileClip

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper


@log_time
def main():
    source_path = os.getenv('SOURCE_PATH')
    if not source_path or not os.path.isfile(source_path):
        logging.error("SOURCE_PATH is not set or the file does not exist.")
        return

    logging.info(f"Converting: {source_path}")
    try:
        video = VideoFileClip(source_path)
        output_path = "output_audio.mp3"
        video.audio.write_audiofile(output_path)
        logging.info(f"Saved MP3 to: {output_path}")
    except Exception as e:
        logging.exception(f"Conversion failed: {e}")

if __name__ == "__main__":
    main()
