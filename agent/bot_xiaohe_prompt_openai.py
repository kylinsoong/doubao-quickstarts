import os
from tldextract import extract
from openai import OpenAI
   
def extract_second_level_domain(url):
    parsed = extract(url)
    return f"{parsed.domain}.{parsed.suffix}" if parsed.domain and parsed.suffix else None


client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3/bots",
    api_key=os.environ.get("ARK_API_KEY")
)


prompt = "过度运动可能有害健康"

completion = client.chat.completions.create(
    model=os.environ.get("ARK_BOT_ID"),
    messages = [
        {"role": "user", "content": prompt},
    ],
)


result = completion.choices[0].message.content + "\n\n"

resources = []
for r in completion.references:
    #print(r["url"])
    resources.append(extract_second_level_domain(r["url"]))

ending = "**内容来源:** " + str(set(resources))

result = result + ending

print(result)
