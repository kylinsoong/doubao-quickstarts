import os
import uuid

from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL

coze_api_token = os.getenv("COZE_API_TOKEN")

coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=COZE_CN_BASE_URL)


bot_id = "7511923863467704357"

user_id = str(uuid.uuid4()) 

for event in coze.chat.stream(bot_id=bot_id, user_id=user_id, additional_messages=[Message.build_user_question_text("如何查看月对账单")]):
    if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
        message = event.message
        #print(f"role={message.role}, content={message.content}") 
        print(message.content, end="") 

print()

