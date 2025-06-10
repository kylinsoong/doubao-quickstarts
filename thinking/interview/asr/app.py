from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

base_url = 'https://openspeech.bytedance.com/api/v1/vc'
language = 'zh-CN'

def ac_video_caption(appid, access_token, video_file_url):
    response = requests.post(
        f'{base_url}/submit',
        params=dict(
            appid=appid,
            language=language,
            use_itn='True',
            use_capitalize='True',
            max_lines=1,
            words_per_line=15,
        ),
        json={
            'url': video_file_url,
        },
        headers={
            'content-type': 'application/json',
            'Authorization': f'Bearer; {access_token}'
        }
    )
    print('submit response = {}'.format(response.text))
    assert response.status_code == 200
    assert response.json()['message'] == 'Success'

    job_id = response.json()['id']
    response = requests.get(
        f'{base_url}/query',
        params=dict(
            appid=appid,
            id=job_id,
        ),
        headers={
            'Authorization': f'Bearer; {access_token}'
        }
    )
    assert response.status_code == 200
    utterances = response.json()
    return utterances

@app.route('/citic/asr', methods=['POST'])
def asr():
    data = request.get_json()
    appid = data.get('appid')
    access_token = data.get('access_token')
    file_url = data.get('file_url')

    if not all([appid, access_token, file_url]):
        return jsonify({"error": "appid, access_token and file_url are required"}), 400

    result = ac_video_caption(appid, access_token, file_url)
    results = []
    if 'utterances' in result:
        utterances = result['utterances']
        for item in utterances:
            start_time = round(item['start_time'] / 1000, 2)
            end_time = round(item['end_time'] / 1000, 2)
            utterance = {
                "start_time": start_time,
                "end_time": end_time,
                "text": item['text']
            }
            results.append(utterance)

    response = jsonify(results)
    response_str = response.get_data(as_text=True)
    #print(type(response_str))
    return response_str

if __name__ == '__main__':
    app.run(debug=True)
