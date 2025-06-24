import time
import os
import json
import requests

base_url = 'https://openspeech.bytedance.com/api/v1/vc/ata'
appid = os.getenv("X_API_APPID")
access_token = os.getenv("X_API_TOKEN")
file_url = "https://yqszhyx.oss-cn-hangzhou.aliyuncs.com/yljk_yqszhyx/promoto/audio/D3PqA5/198517-4.mp3"
audio_text = "早期食管癌手术治疗的方式有哪些？\n我们应该如何选择？\n食管癌早期还是以手术治疗为主，\n以A期、一B期和二期属于比较早期。\n现在最早期的EA期，\n也就是当食管癌局限于食管黏膜层，\n这种的微创手术是通过内镜来做，\n也就是在胃镜的引导下来把食管的黏膜做一个切除，\n这种微创手术应该说是真正意义上的微创。\n患者可能身体没有伤口，\n只是在胃镜下把这一段食管的病变黏膜做一个切除就可以。\n另外一B期或者说是二期的食管癌，\n就需要采取外科手术。\n外科手术传统就是开胸，\n要把食管切除，\n把胃做一个管状胃的这一个采取把胃上提。\n近些年这种传统的开放手术基本上被替代了。\n现在这种食管手术还是以胸腹腔镜包括机器人的手术迅速的发展。\n因为这些腔镜包括机器人的手术要相对于传统开胸手术它更有优势。\n一个是切口小，\n患者痛苦比较小，\n术后这种疼痛要比传统的手术减轻很低。\n另外这种微创手术，\n因为它能进一个摄像头到胸腔和腹腔，\n能在放大的模式下操作这个手术。\n无论是肿瘤的切除，\n还有淋巴结的清扫，\n都要比传统的手术有优势。\n术后患者恢复会比较快，\n出血也比较少。\n还有腹腔镜联合不开胸，\n在颈部和腹部有切口就可以把肿瘤彻底切除。\n当然这个技术现在近几年才兴起，\n需要特别有经验，\n技术水平比较高的专业医生来操作。\n总体来说食管癌早期它是以手术治疗为主，\n目前的手术方式包括了内镜、\n胸腹腔镜，\n还有达芬奇机器人以及纵隔镜。\n各个手术方式各有优缺点，\n是需要专业的医生来准确的判断哪一种治疗方式更适合患者，\n能让患者最大程度的减少痛苦，\n避免并发症，\n取得一个好的康复效果，\n回归健康的生活。"


def log_time(func):
    def wrapper(*args, **kw):
        begin_time = time.time()
        func(*args, **kw)
        print('total cost time = {time}'.format(time=time.time() - begin_time))
    return wrapper


@log_time
def main():
    response = requests.post(
        '{base_url}/submit'.format(base_url=base_url),
        params=dict(
            appid=appid,
            caption_type='speech',
        ),
        json={
            'audio_text': audio_text,
            'url': file_url,
        },
        headers={
            'Authorization': 'Bearer; {}'.format(access_token)
        }
    )
    print('submit response = {}'.format(response.text))
    assert (response.status_code == 200)
    assert (response.json()['message'] == 'Success')

    #time.sleep(10)

    job_id = response.json()['id']
    response = requests.get(
        '{base_url}/query'.format(base_url=base_url),
        params=dict(
            appid=appid,
            id=job_id,
        ),
        headers={
            'Authorization': 'Bearer; {}'.format(access_token)
        }
    )
    print('query response = {}'.format(response.json()))
    assert (response.status_code == 200)

    with open('response.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False)


if __name__ == '__main__':
    main()
