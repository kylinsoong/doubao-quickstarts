import json

def ms_to_min_sec(milliseconds):
    total_seconds = int(milliseconds // 1000)
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"


with open('response.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

utterances = data.get('utterances', [])

for utterance in utterances:
    utterance.pop('words', None)
    utterance.pop('attribute', None)
    utterance['start_time'] = ms_to_min_sec(utterance['start_time'])
    utterance['end_time'] = ms_to_min_sec(utterance['end_time'])

print(json.dumps(utterances, ensure_ascii=False))

with open('utterances.json', 'w', encoding='utf-8') as output_file:
    json.dump(utterances, output_file, ensure_ascii=False)
