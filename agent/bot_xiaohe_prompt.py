import os
from volcenginesdkarkruntime import Ark
from tldextract import extract
   
def extract_second_level_domain(url):
    parsed = extract(url)
    return f"{parsed.domain}.{parsed.suffix}" if parsed.domain and parsed.suffix else None

client = Ark(
    api_key = os.environ.get("ARK_API_KEY")
)

prompt = "过度运动可能有害健康"

completion = client.bot_chat.completions.create(
    model=os.environ.get("ARK_BOT_ID"),
    messages = [
        {"role": "user", "content": prompt},
    ],
)


result = completion.choices[0].message.content + "\n\n"

resources = []
for r in completion.references:
    resources.append(extract_second_level_domain(r.url))

ending = "**内容来源:** " + str(set(resources))

result = result + ending

print(result)
