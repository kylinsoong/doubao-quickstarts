import os

from cozepy import COZE_COM_BASE_URL, COZE_CN_BASE_URL
from cozepy.auth import JWTAuth

#coze_api_base = os.getenv("COZE_API_BASE") or COZE_COM_BASE_URL

coze_api_base = COZE_CN_BASE_URL

# client ID
jwt_oauth_client_id = os.getenv("COZE_JWT_OAUTH_APP_ID")
# private key
jwt_oauth_private_key = os.getenv("COZE_JWT_OAUTH_PRIVATE_KEY")
# path to the private key file (usually with .pem extension)
jwt_oauth_private_key_file_path = os.getenv("COZE_JWT_OAUTH_PRIVATE_KEY_FILE_PATH")
# public key id
jwt_oauth_public_key_id = os.getenv("COZE_JWT_OAUTH_PUBLIC_KEY_ID")

if jwt_oauth_private_key_file_path:
    with open(jwt_oauth_private_key_file_path, "r") as f:
        jwt_oauth_private_key = f.read()


from cozepy import Coze, TokenAuth, JWTOAuthApp  # noqa

jwt_oauth_app = JWTOAuthApp(
    client_id=jwt_oauth_client_id,
    private_key=jwt_oauth_private_key,
    public_key_id=jwt_oauth_public_key_id,
    base_url=coze_api_base,
)

oauth_token = jwt_oauth_app.get_access_token(ttl=3600)

print(oauth_token)

