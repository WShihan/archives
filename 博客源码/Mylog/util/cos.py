# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


class COSOption:
    def __init__(
        self,
        bucket: str = None,
        secretid: str = None,
        secretkey: str = None,
        region: str = 'ap-nanjing',
        scheme: str = 'https',
    ):
        self.bucket = bucket
        self.region = region
        self.secretid = secretid
        self.secretkey = secretkey
        self.scheme = scheme


class COS:
    def __init__(self, cos_url: str):
        custom_config = self.parse_config(cos_url)
        self.__config = CosConfig(
            Region=custom_config.region,
            SecretId=custom_config.secretid,
            SecretKey=custom_config.secretkey,
            Scheme=custom_config.scheme,
        )
        self.__client = CosS3Client(self.__config)
        self.__bucket = custom_config.bucket
        self.__production = True
        self.__one_base_url = (
            f'https://{self.__bucket}.cos.{custom_config.region}.myqcloud.com/one/'
        )

    @property
    def one_baseurl(self):
        return self.__one_base_url

    @property
    def production(self):
        return self.__production

    @production.setter
    def production(self, val: bool):
        self.__production = val

    @property
    def path_thumb(self):
        if self.production:
            return '/maphoto/thumb/'
        else:
            return '/test/thumb/'

    @property
    def path_photo(self):
        if self.production:
            return '/maphoto/photos/'
        else:
            return '/test/photos/'

    @property
    def path_one(self):
        if self.__production:
            return '/one/'
        else:
            return '/test/'

    def parse_config(self, cos_url) -> COSOption:
        config = cos_url.split(';')
        config_dic = {c.split('=')[0]: c.split('=')[1] for c in config}
        return COSOption(**config_dic)

    def post(self, fp, key: str) -> dict:
        return self.__client.put_object(
            Bucket=self.__bucket,
            Body=fp,
            Key=key,
            EnableMD5=False,
            ContentType='multipart/form-data',
        )

    def post2thumb(self, fp, file_name: str) -> dict:
        return self.__client.put_object(
            Bucket=self.__bucket,
            Body=fp,
            Key=self.path_thumb + file_name,
            EnableMD5=False,
            ContentType='multipart/form-data',
        )

    def post2photo(self, fp, file_name: str) -> dict:
        resp = self.__client.put_object(
            Bucket=self.__bucket,
            Body=fp,
            Key=self.path_photo + file_name,
            EnableMD5=False,
            ContentType='multipart/form-data',
        )
        return resp

    def post2one(self, fp, file_name: str):
        return self.__client.put_object(
            Bucket=self.__bucket,
            Body=fp,
            Key=self.path_one + file_name,
            EnableMD5=False,
            ContentType='multipart/form-data',
        )

    def exists(self, key) -> bool:
        return self.__client.object_exists(Bucket=self.__bucket, Key=key)


if __name__ == '__main__':
    c = COS('')
    c.production = True
    res = c.exists('lora.png')
    print(res)
    with open('./lora.png', 'rb') as f:
        res = c.post2photo(f, 'lora.jpg')
        print(res)
