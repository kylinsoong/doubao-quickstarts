import os
import json
from volcengine import visual
from volcengine.visual.VisualService import VisualService


AK = os.getenv("VE_AK")
SK = os.getenv("VE_SK")


visual_service = VisualService()
visual_service.set_ak(AK)
visual_service.set_sk(SK)


form = {
    "req_key": "high_aes_general_v21_L",
    "task_id": "7470418866540478502",
    "return_url": True,
    "req_json": "{\"logo_info\":{\"add_logo\":true，\"position\":1, \"language\":1,\"opacity\"：0.5}}"
}


resp = visual_service.cv_sync2async_get_result(form)

print(resp)
