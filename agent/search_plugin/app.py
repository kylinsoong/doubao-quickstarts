import os
import json
from flask import Flask, request
from flask import jsonify
from volcenginesdkarkruntime import Ark

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False 


@app.route('/query_internet_search', methods=['POST'])
def query_internet_search():
    data = request.get_json()
    API_KEY = os.environ.get("ARK_API_KEY")
    query = data.get("query")

    print("query:", query)

    if not API_KEY:
        return json.dumps({"error": "Missing api_key or endpoint"}), 400

    client = Ark(api_key=API_KEY)

    completion = client.bot_chat.completions.create(
        model="bot-20250812141711-xb7bd",
        messages = [
            {"role": "user", "content": query},
           ],
    )

    content = completion.choices[0].message.content
    #print(type(content))

    #print(content)

    return {"result": content}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
