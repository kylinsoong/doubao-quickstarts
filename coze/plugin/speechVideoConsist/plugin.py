from runtime import Args
from typings.speechVideoConsist.speechVideoConsist import Input, Output
import requests
import logging

def vc_video_caption(video_file_url, appid, access_token):
    logging.info(f"process: {video_file_url}")
    language = 'zh-CN'
    base_url = 'https://openspeech.bytedance.com/api/v1/vc'
    response = requests.post(
                 '{base_url}/submit'.format(base_url=base_url),
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
                    'Authorization': 'Bearer; {}'.format(access_token)
                 }
             )
    logging.info('submit response = {}'.format(response.text))

    if response.status_code != 200:
        logging.error(f"Failed to submit video. HTTP status code: {response.status_code}, Response: {response.text}")
        return []

    response_json = response.json()

    if response_json.get('message') != 'Success':
        logging.error(f"Submission unsuccessful. Message: {response_json.get('message')}")
        return []


    job_id = response.json()['id']

    if not job_id:
            logging.error(f"Job ID not found in response. Response: {response.text}")
            return []

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

    if response.status_code != 200:
        logging.error(f"Failed to query job status. HTTP status code: {response.status_code}, Response: {response.text}")
        return []

    utterances = response.json()['utterances']
    return utterances

"""
Each file needs to export a function named `handler`. This function is the entrance to the Tool.

Parameters:
args: parameters of the entry function.
args.input - input parameters, you can get test input value by args.input.xxx.
args.logger - logger instance used to print logs, injected by runtime.

Remember to fill in input/output in Metadata, it helps LLM to recognize and use tool.

Return:
The return data of the function, which should match the declared output parameters.
"""
def handler(args: Args[Input])->Output:

    video_file_url = args.input.video_file_url
    appid = args.input.appid
    access_token = args.input.access_token
    threshold_ms = args.input.threshold_ms

    utterances = vc_video_caption(video_file_url, appid, access_token)
    interruptions = []
    for i in range(len(utterances) - 1):
        current_end = utterances[i]["end_time"]
        next_start = utterances[i + 1]["start_time"]

        gap = next_start - current_end
        if gap > threshold_ms:
            interruptions.append({
                "gap_duration": gap,
                "gap_start": current_end,
                "gap_end": next_start
            })

    results = []
    if len(interruptions):
        logging.info("字幕检测显示视频不连续(可通过 threshold_ms 设定不连续判断阈值，默认超过 {threshold_ms} 毫秒不说话则认为视频不连续):")
        for i, interrupt in enumerate(interruptions, 1):
            interruptstr = f"中断 {i}: 从 {interrupt['gap_start']} 毫秒 到 {interrupt['gap_end']} 毫秒，" + f"出现 {interrupt['gap_duration']} 毫秒的间隔"
            logging.info(interruptstr)
            results.append(interruptstr)
    else:
        results.append("视频字幕检查该双录视频是连续的")

    return {"message": results}
