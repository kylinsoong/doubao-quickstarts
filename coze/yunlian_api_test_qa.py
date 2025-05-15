import os
import uuid

from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL

coze_api_token = os.getenv("COZE_API_TOKEN")

coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=COZE_CN_BASE_URL)


bot_id = "7504221940052393996"

user_id = str(uuid.uuid4()) 

query = "Hello"

try:
    for event in coze.chat.stream(bot_id=bot_id, user_id=user_id, additional_messages=[Message.build_user_question_text(query)]):
        print(event.event)
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            message = event.message
            print(message.content, end="")
except Exception as e:
    if hasattr(e, '_raw_response'):
        print("Raw response data:", e._raw_response.text)
        print()
    raise

print()

