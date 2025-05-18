import os
import uuid
from typing import Callable, Optional
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL

coze_api_token = os.getenv("COZE_API_TOKEN")

coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=COZE_CN_BASE_URL)

bot_id = "7504221940052393996"

user_id = str(uuid.uuid4()) 

query = "Hello"


def build_hello_conversation_context(coze: Coze, bot_id: str) -> Callable[[str], str]:

    conversation = coze.conversations.create(
        messages=[
            Message.build_user_question_text("输入用户数量"),
            Message.build_assistant_answer("1009"),
        ]
    )

    def hello_conversation_context(text: str) -> str:
        for event in coze.chat.stream(
            bot_id=bot_id,
            user_id=user_id,
            additional_messages=[Message.build_user_question_text(query)],
            conversation_id=conversation.id,
        ):
            if event.event == ChatEventType.CONVERSATION_MESSAGE_COMPLETED:
                return event.message.content

    return hello_conversation_context

hello_func = build_hello_conversation_context(coze, bot_id)

print(hello_func(query))
