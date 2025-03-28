import os
import uuid
import time


from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL

def log_time(func):
    """Decorator to log execution time of a function."""
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function '{func.__name__}' executed in {end_time - begin_time:.2f} seconds")
        return result
    return wrapper

@log_time
def chat_with_caze(query, bot_id="7486350111568871424"):
    coze_api_token = os.getenv("COZE_API_TOKEN")
    coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=COZE_CN_BASE_URL)

    user_id = str(uuid.uuid4())

    for event in coze.chat.stream(
        bot_id=bot_id, 
        user_id=user_id, 
        additional_messages=[Message.build_user_question_text(query)]
    ):
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            message = event.message
            print(message.content, end="")


chat_with_caze("康复医疗行业分析")
print()

