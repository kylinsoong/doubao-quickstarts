import tos
import os

class TosClient:
    # 文档链接：https://www.volcengine.com/docs/6349/92786
    def __init__(self):
       # Access Key访问火山云资源的秘钥，可从访问控制-API访问密钥获取获取
        # 为了保障安全，强烈建议您不要在代码中明文维护您的AKSK
        # 从环境变量中获取访问密钥（AK）
        self.ak = os.environ.get("VE_ACCESS_KEY")
        # 从环境变量中获取秘密密钥（SK）
        self.sk = os.environ.get("VE_SECRET_KEY")
        # your endpoint 和 your region 填写Bucket 所在区域对应的Endpoint。# 以华北2(北京)为例，your endpoint 填写 tos-cn-beijing.volces.com，your region 填写 cn-beijing。
        self.endpoint = "tos-cn-beijing.volces.com"
        self.region = "cn-beijing"
        self.client = tos.TosClientV2(self.ak, self.sk, self.endpoint, self.region)

    def create_bucket(self, bucket_name):
        try:
            # 设置桶存储桶读写权限
            self.client.create_bucket(bucket_name, acl=tos.ACLType.ACL_Public_Read_Write)
        except tos.exceptions.TosClientError as e:
            # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
            print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
        except tos.exceptions.TosServerError as e:
            # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
            print('fail with server error, code: {}'.format(e.code))
            # request id 可定位具体问题，强烈建议日志中保存
            print('error with request id: {}'.format(e.request_id))
            print('error with message: {}'.format(e.message))
            print('error with http code: {}'.format(e.status_code))
            print('error with ec: {}'.format(e.ec))
            print('error with request url: {}'.format(e.request_url))
        except Exception as e:
            print('fail with unknown error: {}'.format(e))

    def put_object_from_file(self, bucket_name, object_key, file_path):
        try:
            # 通过字符串方式添加 Object
            res = self.client.put_object_from_file(bucket_name, object_key, file_path)
        except tos.exceptions.TosClientError as e:
            # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
            print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
        except tos.exceptions.TosServerError as e:
            # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
            print('fail with server error, code: {}'.format(e.code))
            # request id 可定位具体问题，强烈建议日志中保存
            print('error with request id: {}'.format(e.request_id))
            print('error with message: {}'.format(e.message))
            print('error with http code: {}'.format(e.status_code))
            print('error with ec: {}'.format(e.ec))
            print('error with request url: {}'.format(e.request_url))
        except Exception as e:
            print('fail with unknown error: {}'.format(e))

    def get_object(self, bucket_name, object_name):
        try:
            # 下载对象到内存中
            object_stream = self.client.get_object(bucket_name, object_name)
            # object_stream 为迭代器可迭代读取数据
            # for content in object_stream:
            #     print(content)
            # 您也可调用 read()方法一次在内存中获取完整的数据
            print(object_stream.read())
        except tos.exceptions.TosClientError as e:
            # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
            print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
        except tos.exceptions.TosServerError as e:
            # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
            print('fail with server error, code: {}'.format(e.code))
            # request id 可定位具体问题，强烈建议日志中保存
            print('error with request id: {}'.format(e.request_id))
            print('error with message: {}'.format(e.message))
            print('error with http code: {}'.format(e.status_code))
            print('error with ec: {}'.format(e.ec))
            print('error with request url: {}'.format(e.request_url))
        except Exception as e:
            print('fail with unknown error: {}'.format(e))

    def close_client(self):
        try:
            # 执行相关操作后，将不再使用的TosClient关闭
            self.client.close()
        except tos.exceptions.TosClientError as e:
            # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
            print('fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
        except tos.exceptions.TosServerError as e:
            # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
            print('fail with server error, code: {}'.format(e.code))
            # request id 可定位具体问题，强烈建议日志中保存
            print('error with request id: {}'.format(e.request_id))
            print('error with message: {}'.format(e.message))
            print('error with http code: {}'.format(e.status_code))
            print('error with ec: {}'.format(e.ec))
            print('error with request url: {}'.format(e.request_url))
        except Exception as e:
            print('fail with unknown error: {}'.format(e))
