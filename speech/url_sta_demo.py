import time
import requests


base_url = 'https://openspeech.bytedance.com/api/v1/vc/ata'
appid = ""
access_token = ""
file_url = "https://you-domain.com/xxxx.wav"
audio_text = "hello world"


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
            'audio_text': 'hello wolrd',
            'url': file_url,
        },
        headers={
            'Authorization': 'Bearer; {}'.format(access_token)
        }
    )
    print('submit response = {}'.format(response.text))
    assert (response.status_code == 200)
    assert (response.json()['message'] == 'Success')

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


if __name__ == '__main__':
    main()
