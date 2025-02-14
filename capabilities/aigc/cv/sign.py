from datetime import datetime
import json
import hashlib
from urllib.parse import quote
import hmac
import os

AK = os.getenv("VE_AK")
SK = os.getenv("VE_SK")

def norm_query(params):
    query = ""
    for key in sorted(params.keys()):
        if type(params[key]) == list:
            for k in params[key]:
                query = (
                        query + quote(key, safe="-_.~") + "=" + quote(k, safe="-_.~") + "&"
                )
        else:
            query = (query + quote(key, safe="-_.~") + "=" + quote(params[key], safe="-_.~") + "&")
    query = query[:-1]
    return query.replace("+", "%20")

def hmac_sha256(key: bytes, content: str):
    return hmac.new(key, content.encode("utf-8"), hashlib.sha256).digest()


def hash_sha256(content: str):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def read_file(name):
    with open(name,"r", encoding="utf-8") as f:
        form = f.read()
    return form
    
body = json.dumps(read_file("payload.json"))

print(body)


Service = "cv"
Version = "2022-08-31"
Region = "cn-north-1"
Host = "visual.volcengineapi.com"
ContentType = "application/json"
method = "POST"

date  = datetime.utcnow()
action = "CVProcess"
query = {}
header = {}


credential = {
        "access_key_id": AK,
        "secret_access_key": SK,
        "service": Service,
        "region": Region,
}

request_param = {
    "body": body,
    "host": Host,
    "path": "/",
    "method": method,
    "content_type": ContentType,
    "date": date,
    "query": {"Action": action, "Version": Version, **query},
}

x_date = request_param["date"].strftime("%Y%m%dT%H%M%SZ")
short_x_date = x_date[:8]
x_content_sha256 = hash_sha256(request_param["body"])
sign_result = {
        "Host": request_param["host"],
        "X-Content-Sha256": x_content_sha256,
        "X-Date": x_date,
        "Content-Type": request_param["content_type"],
}

signed_headers_str = ";".join(
        ["content-type", "host", "x-content-sha256", "x-date"]
)

canonical_request_str = "\n".join(
        [request_param["method"].upper(),
         request_param["path"],
         norm_query(request_param["query"]),
         "\n".join(
             [
                 "content-type:" + request_param["content_type"],
                 "host:" + request_param["host"],
                 "x-content-sha256:" + x_content_sha256,
                 "x-date:" + x_date,
             ]
         ),
         "",
         signed_headers_str,
         x_content_sha256,
         ]
)

print(canonical_request_str)
hashed_canonical_request = hash_sha256(canonical_request_str)
print(hashed_canonical_request)

credential_scope = "/".join([short_x_date, credential["region"], credential["service"], "request"])
string_to_sign = "\n".join(["HMAC-SHA256", x_date, credential_scope, hashed_canonical_request])


print(string_to_sign)
k_date = hmac_sha256(credential["secret_access_key"].encode("utf-8"), short_x_date)
k_region = hmac_sha256(k_date, credential["region"])
k_service = hmac_sha256(k_region, credential["service"])
k_signing = hmac_sha256(k_service, "request")
signature = hmac_sha256(k_signing, string_to_sign).hex()

sign_result["Authorization"] = "HMAC-SHA256 Credential={}, SignedHeaders={}, Signature={}".format(
        credential["access_key_id"] + "/" + credential_scope,
        signed_headers_str,
        signature,
    )

header = {**header, **sign_result}

print()

print(header)






