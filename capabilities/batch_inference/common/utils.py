import binascii
import datetime
import hashlib
import hmac
import urllib
from typing import Dict


def get_volc_signature(secret_key, data):
    return hmac.new(secret_key, data.encode('utf-8'), digestmod=hashlib.sha256).digest()


def get_hmac_encode16(data) -> str:
    return binascii.b2a_hex(hashlib.sha256(data.encode('utf-8')).digest()).decode('ascii')


def get_canonical_query_string(param_dict) -> str:
    target = sorted(param_dict.items(), key=lambda x: x[0], reverse=False)
    canonicalQueryString = urllib.parse.urlencode(target)
    return canonicalQueryString


def get_hmac_encode16_noencode(data) -> str:
    return binascii.b2a_hex(hashlib.sha256(data).digest()).decode('ascii')


def get_hashmac_headers(domain, region, service, canonicalquerystring, httprequestmethod, canonicaluri,
                        contenttype, payloadsign, ak, sk) -> Dict[str, any]:
    utc_time_sencond = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
    utc_time_day = datetime.datetime.utcnow().strftime('%Y%m%d')
    credentialScope = utc_time_day + '/' + region + '/' + service + '/request'
    headers = {
        'content-type': contenttype,
        'x-date': utc_time_sencond,
    }
    canonicalHeaders = 'content-type:' + contenttype + '\n' \
                       + 'host:' + domain + '\n' + 'x-content-sha256:' \
                       + '\n' + 'x-date:{}'.format(utc_time_sencond) + '\n'
    signedHeaders = 'content-type;host;x-content-sha256;x-date'
    canonicalRequest = httprequestmethod + '\n' + canonicaluri + '\n' + canonicalquerystring \
                       + '\n' + canonicalHeaders + '\n' + signedHeaders + '\n' + payloadsign
    stringToSign = 'HMAC-SHA256' + '\n' + utc_time_sencond + '\n' + credentialScope + '\n' \
                   + get_hmac_encode16(canonicalRequest)
    signingkey = get_volc_signature(
        get_volc_signature(get_volc_signature(get_volc_signature(sk.encode('utf-8'), utc_time_day), region), service),
        'request')
    signature = binascii.b2a_hex(get_volc_signature(signingkey, stringToSign)).decode('ascii')
    headers['Authorization'] = 'HMAC-SHA256 Credential={}/{}, SignedHeaders={}, Signature={}'.format(ak,
                                                                                                     credentialScope,
                                                                                                     signedHeaders,
                                                                                                     signature)
    return headers
