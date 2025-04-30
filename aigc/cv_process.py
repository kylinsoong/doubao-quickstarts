import os
from volcengine.visual.VisualService import VisualService


AK = os.getenv("VE_AK")
SK = os.getenv("VE_SK")


visual_service = VisualService()
visual_service.set_ak(AK)
visual_service.set_sk(SK)

form = {
    "req_key": "face_swap3_6",
    "image_urls": [
        "https://pub-kylin.tos-cn-beijing.volces.com/aigc/female.jpg", "https://pub-kylin.tos-cn-beijing.volces.com/aigc/forest.jpg"
    ],
    "face_type": "area",
    "return_url": True,
    "logo_info": {
        "add_logo": True,
        "position": 0,
        "language": 0,
        "opacity": 0.3,
        "logo_text_content": "KYLIN"
    }
}

resp = visual_service.cv_process(form)
print(resp)
