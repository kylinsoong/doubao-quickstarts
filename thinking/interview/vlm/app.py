import os
import json
from flask import Flask, request
from volcenginesdkarkruntime import Ark

app = Flask(__name__)


@app.route('/avlm', methods=['POST'])
def analyze_video():
    data = request.get_json()
    API_KEY = data.get("api_key")
    API_EP_ID = data.get("endpoint")
    prompt = data.get("prompt")
    video_url = data.get("video_url")

    if not API_KEY or not API_EP_ID:
        return json.dumps({"error": "Missing api_key or endpoint"}), 400

    client = Ark(api_key=API_KEY)

    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "video_url",
                        "video_url": {
                            "url": video_url,
                            "fps": 0.5,
                            "detail": "low"
                        }
                    },
                ],
            }
        ],
        thinking={
            "type": "disabled"
        }
    )

    return completion.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)

