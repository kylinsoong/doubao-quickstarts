import os
from volcengine.visual.VisualService import VisualService


AK = os.getenv('ARK_ACCESS_KEY')
SK = os.getenv('ARK_SECRET_KEY')


visual_service = VisualService()
visual_service.set_ak(AK)
visual_service.set_sk(SK)

form = {
    "req_key": "high_aes_general_v21_L",
    "prompt": "东方美人，桥边姑娘，眼神犹豫中充满力",
    "model_version": "general_v2.1_L",
    "req_schedule_conf": "general_v20_9B_pe",
    "llm_seed": -1,
    "seed": -1,
    "scale": 3.5,
    "ddim_steps": 25,
    "width": 512,
    "height": 512,
    "use_pre_llm": True,
    "use_sr": True,
    "sr_seed": -1,
    "sr_strength": 0.4,
    "sr_scale": 3.5,
    "sr_steps": 20,
    "is_only_sr": False,
    "return_url": True,
    "logo_info": {
        "add_logo": False,
        "position": 0,
        "language": 0,
        "opacity": 0.3,
        "logo_text_content": "这里是明水印内容"
    }
}

resp = visual_service.cv_process(form)
print(resp)
