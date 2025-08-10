import os
import uuid
import time
from flask import Flask, request
from flask_cors import CORS 
from cozepy import Coze, TokenAuth, JWTOAuthApp, Message, ChatStatus, MessageContentType, ChatEventType, COZE_CN_BASE_URL, COZE_COM_BASE_URL
from cozepy.auth import JWTAuth

app = Flask(__name__)
CORS(app, resources=r"/*")  

def get_coze_api_base() -> str:
    coze_api_base = os.getenv("COZE_API_BASE")
    if coze_api_base:
        return coze_api_base

    return COZE_CN_BASE_URL 


def get_auth_token():

    coze_api_base = os.getenv("COZE_API_BASE") or COZE_CN_BASE_URL

    jwt_oauth_client_id = os.getenv("COZE_JWT_OAUTH_APP_ID") or "1152759474689"
    jwt_oauth_private_key = os.getenv("COZE_JWT_OAUTH_PRIVATE_KEY") or "private_key.pem"
    jwt_oauth_private_key_file_path = os.getenv("COZE_JWT_OAUTH_PRIVATE_KEY_FILE_PATH") or "/app/keys/private_key.pem"
    jwt_oauth_public_key_id = os.getenv("COZE_JWT_OAUTH_PUBLIC_KEY_ID") or "mucgAQkJawg7lxMH5cvTfD7Li0_y9-tEbFH4kPiytko"

    if jwt_oauth_private_key_file_path:
        with open(jwt_oauth_private_key_file_path, "r") as f:
            jwt_oauth_private_key = f.read()

    jwt_oauth_app = JWTOAuthApp(
        client_id=jwt_oauth_client_id,
        private_key=jwt_oauth_private_key,
        public_key_id=jwt_oauth_public_key_id,
        base_url=coze_api_base,
    )

    oauth_token = jwt_oauth_app.get_access_token(ttl=1800)

    return oauth_token.access_token


def coze_chat_interaction(
    query,
    bot_id=None,
    user_id="",
    is_debug=None,
    run_step_by_step=None,
    timeout=600  
):

    """
    Interact with Coze bot using the provided parameters.
    
    Args:
        bot_id (str, optional): Coze bot ID. If not provided, uses COZE_BOT_ID environment variable.
        user_id (str): User identifier for the chat session.
        is_debug (bool, optional): Enable debug logging. If None, uses DEBUG environment variable.
        run_step_by_step (bool, optional): Use step-by-step chat handling. If None, uses RUN_STEP_BY_STEP environment variable.
        timeout (int): Maximum time (seconds) to wait for chat completion.
        
    Returns:
        dict: Contains chat status, messages, and token usage if available.
    """
    # Initialize Coze client
    coze = Coze(
        auth=TokenAuth(token=get_auth_token()),
        base_url=get_coze_api_base()
    )
    
    # Resolve bot ID from parameter or environment variable
    bot_id = bot_id or os.getenv("COZE_BOT_ID") or "7531696470618554419"
    
    # Resolve debug flag from parameter or environment variable
    is_debug = is_debug if is_debug is not None else os.getenv("DEBUG")
    if is_debug:
        setup_logging(logging.DEBUG)
    
    # Resolve step-by-step flag from parameter or environment variable
    run_step_by_step = run_step_by_step if run_step_by_step is not None else os.getenv("RUN_STEP_BY_STEP")
    
    # Prepare conversation messages
    messages = [
        Message.build_user_question_text(query),
    ]
    
    result = {
        "status": None,
        "messages": [],
        "token_usage": None
    }
    
    try:
        if run_step_by_step:
            # Create initial chat
            chat = coze.chat.create(
                bot_id=bot_id,
                user_id=user_id,
                additional_messages=messages
            )
            
            # Poll for chat completion
            start_time = int(time.time())
            while chat.status == ChatStatus.IN_PROGRESS:
                if int(time.time()) - start_time > timeout:
                    coze.chat.cancel(
                        conversation_id=chat.conversation_id,
                        chat_id=chat.id
                    )
                    result["status"] = "TIMEOUT"
                    return result
                
                time.sleep(1)
                chat = coze.chat.retrieve(
                    conversation_id=chat.conversation_id,
                    chat_id=chat.id
                )
            
            # Get all messages from completed chat
            chat_messages = coze.chat.messages.list(
                conversation_id=chat.conversation_id,
                chat_id=chat.id
            )
            message_list = chat_messages.data
            message_strings = []
            for msg in message_list:
                message_strings.append(msg.content)

            result["messages"] = "\n".join(message_strings)            
            result["status"] = chat.status.name
            
        else:
            # Use simplified create_and_poll method
            chat_poll = coze.chat.create_and_poll(
                bot_id=bot_id,
                user_id=user_id,
                additional_messages=messages
            )

            message_list = chat_poll.messages
            message_strings = []
            for msg in message_list:
                message_strings.append(msg.content)

            result["messages"] = message_strings[0]
            
            #result["messages"] = chat_poll.messages
            result["status"] = chat_poll.chat.status.name
            
            # Capture token usage if available
            if chat_poll.chat.status == ChatStatus.COMPLETED:
                result["token_usage"] = chat_poll.chat.usage.token_count
    
    except Exception as e:
        result["status"] = "ERROR"
        result["error"] = str(e)
    
    return result


@app.route('/qa', methods=['GET'])
def qa_endpoint():
    query = request.args.get('query')
    if not query:
        return "缺少参数: query", 400

    print("received new query", query)
    
    user_id = str(uuid.uuid1())
    
    result = coze_chat_interaction(query=query, user_id=user_id)
    
    print(result)
    
    if result["status"] == "ERROR":
        return f"错误: {result['error']}", 500
    elif result["status"] == "TIMEOUT":
        return "请求超时", 408
    elif not result["messages"]:
        return "未获取到回复", 500
    
    return result["messages"]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
