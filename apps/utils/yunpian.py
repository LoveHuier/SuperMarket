# _*_coding: utf-8_*_
import requests
import json


class YunPian:
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【Mata云超市】您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url, parmas)

        re_dict = json.loads(response.text)
        return re_dict


if __name__ == "__main__":
    yp = YunPian(api_key="a4c4b702730cce7ba544ccb96452436d")
    yp.send_sms(code="112233", mobile="13909283431")
