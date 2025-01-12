import os


python_files = [
    "ark_vision_image_analysis.py",
    "ark_vision_image_analysis_encording.py",
    "ark_vision_image_analysis_er.py",
    "ark_vision_image_analysis_high.py",
    "ark_vision_image_analysis_math.py",
    "ark_vision_image_analysis_medical.py",
    "ark_vision_images_analysis.py",
    "ark_vision_images_analysis_difference.py",
    "ark_vision_images_analysis_glasses.py",
    "ark_vision_image_chart_pie.py",
    "ark_vision_images_nutritions.py",
    "ark_vision_images_sky-grass.py",
    "ark_vision_images_foods_cook.py",
    "ark_vision_images_sales.py",
    "ark_vision_image_homework.py",
    "ark_vision_image_wechat.py",
    "ark_vision_image_dianping.py"
]


for file in python_files:
    try:
        os.system(f"python3 {file}")
    except Exception as e:
        print(f"Error running {file}: {e}")
