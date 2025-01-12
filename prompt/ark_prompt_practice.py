import os
from volcenginesdkarkruntime import Ark

API_KEY = os.environ.get("ARK_API_KEY")
API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

client = Ark(api_key=API_KEY)

def chat_completion(prompt):
    completion = client.chat.completions.create(
        model=API_EP_ID,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message.content)

prompt = "What do you think could be a good name for a flower shop that specializes in selling bouquets of dried flowers more than fresh flowers?"
chat_completion(prompt)

print("=====================")

prompt = "Suggest a name for a flower shop that sells bouquets of dried flowers"
chat_completion(prompt)

print("------------------------------------------------")

prompt = "Tell me about Earth"
chat_completion(prompt)

print("=====================")

prompt = "Generate a list of ways that makes Earth unique compared to other planets"
chat_completion(prompt)

print()
print("------------------------------------------------")


prompt = "What's the best method of boiling water and why is the sky blue?"
chat_completion(prompt)

print("=====================")

prompt = "What's the best method of boiling water?"
chat_completion(prompt)

prompt = "Why is the sky blue?"
chat_completion(prompt)

print()
print("------------------------------------------------")

prompt = "I'm a high school student. Recommend me a programming activity to improve my skills."
chat_completion(prompt)

print("=====================")

prompt = """I'm a high school student. Which of these activities do you suggest and why:
a) learn Python
b) learn JavaScript
c) learn Fortran
"""
chat_completion(prompt)

print()
print("------------------------------------------------")

prompt = """Decide whether a Tweet's sentiment is positive, neutral, or negative.

Tweet: I loved the new YouTube video you made!
Sentiment:
"""
chat_completion(prompt)

print("=====================")

prompt = """Decide whether a Tweet's sentiment is positive, neutral, or negative.

Tweet: I loved the new YouTube video you made!
Sentiment: positive

Tweet: That was awful. Super boring 😠
Sentiment:
"""
chat_completion(prompt)

print("=====================")

prompt = """Decide whether a Tweet's sentiment is positive, neutral, or negative.

Tweet: I loved the new YouTube video you made!
Sentiment: positive

Tweet: That was awful. Super boring 😠
Sentiment: negative

Tweet: Something surprised me about this video - it was actually original. It was not the same old recycled stuff that I always see. Watch it - you will not regret it.
Sentiment:
"""
chat_completion(prompt)
