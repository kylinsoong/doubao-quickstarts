import json
from typing import Dict, Any
import aiohttp
import backoff
from common import utils
import os

class BatchInferenceClient:
    def __init__(self):
        """
        初始化BatchInferenceClient类的实例。
        该方法设置了一些默认属性，如重试次数、超时时间、访问密钥（AK/SK）、账号ID、API版本、服务域名、区域和基础参数。
        访问密钥（AK/SK）从环境变量中获取，以提高安全性。
        基础参数包括API版本和账号ID，这些参数在每次请求中都会用到。
        """
        # 设置重试次数为3次
        self._retry = 3
        # 设置请求超时时间为60秒
        self._timeout = aiohttp.ClientTimeout(60)
        # Access Key访问火山云资源的秘钥，可从访问控制-API访问密钥获取获取
        # 为了保障安全，强烈建议您不要在代码中明文维护您的AKSK
        # 从环境变量中获取访问密钥（AK）
        self.ak = os.environ.get("VE_ACCESS_KEY")
        # 从环境变量中获取秘密密钥（SK）
        self.sk = os.environ.get("VE_SECRET_KEY")
        # 设置模型名称
        self.model = "doubao-pro-32k"
        # 设置模型版本
        self.model_version = "250115"
        # 需要替换为您的账号id，可从火山引擎官网点击账号头像，弹出框中找到，复制“账号ID”后的一串数字
        self.account_id = os.environ.get("VE_ACCOUNT_ID")
        # 设置API版本
        self.version = "2025-01-25"
        # 设置服务域名
        self.domain = "open.volcengineapi.com"
        # 设置区域
        self.region = "cn-beijing"
        # 设置服务名称
        self.service = "ark"
        # 设置基础参数，包括API版本和账号ID
        self.base_param = {"Version": self.version, "X-Account-Id": self.account_id}

    async def _call(self, url, headers, req: Dict[str, Any]):
        """
        异步调用指定URL的HTTP POST请求，并处理请求的重试逻辑。
        :param url: 请求的目标URL。
        :param headers: 请求的HTTP头部信息。
        :param req: 请求的JSON格式数据。
        :return: 响应的JSON数据。
        :raises Exception: 如果请求失败或解析响应失败，抛出异常。
        """
        @backoff.on_exception(
            backoff.expo, Exception, factor=0.1, max_value=5, max_tries=self._retry
        )
        async def _retry_call(body):
            """
            内部函数，用于发送HTTP POST请求，并处理请求的重试逻辑。
            :param body: 请求的JSON格式数据。
            :return: 响应的JSON数据。
            :raises Exception: 如果请求失败或解析响应失败，抛出异常。
            """
            async with aiohttp.request(
                method="POST",
                url=url,
                json=body,
                headers=headers,
                timeout=self._timeout,
            ) as response:
                try:
                    return await response.json()
                except Exception as e:
                    raise e

        try:
            return await _retry_call(req)
        except Exception as e:
            raise e

    async def create_batch_inference_job(
        self, bucket_name, input_object_key, output_object_key: str
    ):
        """
        异步创建批量推理任务。
        :param bucket_name: 存储桶名称。
        :param input_object_key: 输入文件的对象键。
        :param output_object_key: 输出文件的对象键。
        :return: 响应的JSON数据。
        :raises Exception: 如果请求失败或解析响应失败，抛出异常。
        """
        action = "CreateBatchInferenceJob"
        canonicalQueryString = "Action={}&Version={}&X-Account-Id={}".format(
            action, self.version, self.account_id
        )
        url = "https://" + self.domain + "/?" + canonicalQueryString
        extra_param = {
            "Action": action,
            "ProjectName": "default",
            "Name": "just_test",
            "ModelReference": {
                "FoundationModel": {"Name": self.model, "ModelVersion": self.model_version},
            },
            "InputFileTosLocation": {
                "BucketName": bucket_name,
                "ObjectKey": input_object_key,
            },
            "OutputDirTosLocation": {
                "BucketName": bucket_name,
                "ObjectKey": output_object_key,
            },
            "CompletionWindow": "3d",
        }
        param = self.base_param | extra_param

        payloadSign = utils.get_hmac_encode16(json.dumps(param))
        headers = utils.get_hashmac_headers(
            self.domain,
            self.region,
            self.service,
            canonicalQueryString,
            "POST",
            "/",
            "application/json; charset=utf-8",
            payloadSign,
            self.ak,
            self.sk,
        )
        return await self._call(url, headers, param)

    async def ListBatchInferenceJobs(self, phases=None):
        """
        异步列出批量推理任务。
        :param phases: 任务阶段列表，默认为空列表。
        :return: 响应的JSON数据。
        :raises Exception: 如果请求失败或解析响应失败，抛出异常。
        """
        # 如果phases为None，则初始化为空列表
        if phases is None:
            phases = []
        # 设置操作名称为ListBatchInferenceJobs
        action = "ListBatchInferenceJobs"
        # 构建规范查询字符串，包含操作名称、API版本和账号ID
        canonicalQueryString = "Action={}&Version={}&X-Account-Id={}".format(
            action, self.version, self.account_id
        )
        # 构建请求URL
        url = "https://" + self.domain + "/?" + canonicalQueryString
        # 构建额外参数，包括操作名称、项目名称和过滤器
        extra_param = {
            "Action": action,
            "ProjectName": "default",
            "Filter": {"Phases": phases},
        }
        # 合并基础参数和额外参数
        param = self.base_param | extra_param

        # 计算请求体的签名
        payloadSign = utils.get_hmac_encode16(json.dumps(param))
        # 获取请求头，包含签名信息
        headers = utils.get_hashmac_headers(
            self.domain,
            self.region,
            self.service,
            canonicalQueryString,
            "POST",
            "/",
            "application/json; charset=utf-8",
            payloadSign,
            self.ak,
            self.sk,
        )
        # 调用_call方法发送请求并返回响应
        return await self._call(url, headers, param)

        headers = utils.get_hashmac_headers(
            self.domain,
            self.region,
            self.service,
            canonicalQueryString,
            "POST",
            "/",
            "application/json; charset=utf-8",
            payloadSign,
            self.ak,
            self.sk,
        )
        return await self._call(url, headers, param)
