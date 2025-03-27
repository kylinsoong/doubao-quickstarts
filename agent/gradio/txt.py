import gradio as gr
from openai import OpenAI
import os

API_KEY = os.environ.get("ARK_API_KEY")

client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=os.environ.get("ARK_API_KEY"),
)

API_EP_ID = os.environ.get("ARK_API_ENGPOINT_ID")

def chat_with_doubao(messages):

    try:
        completion = client.chat.completions.create(
            model=API_EP_ID,
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"


def chat_interface(user_input, history):
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]
    for user_msg, bot_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    
    print(type(history), len(history))
    messages.append({"role": "user", "content": user_input})
    bot_response = chat_with_doubao(messages)
    return bot_response

with gr.Blocks(title="CHATBOT", css=".gradio-container { width: 100% !important; }") as demo:
    gr.Markdown("<h1 style='text-align: center;'>Chat with Doubao</h1>") 
    gr.ChatInterface(chat_interface)

demo.launch()

