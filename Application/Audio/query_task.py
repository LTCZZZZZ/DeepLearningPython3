# 百度智能云-语音识别-长语音识别-查询识别结果
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
import requests
import json
from tools.connection import config_dict

baidu_config = config_dict('baidu')
API_KEY = baidu_config['API_KEY']
SECRET_KEY = baidu_config['SECRET_KEY']
# print(API_KEY)
# print(SECRET_KEY)


def main():
    url = "https://aip.baidubce.com/rpc/2.0/aasr/v1/query?access_token=" + get_access_token()

    data = {
        "task_ids": [
            # '64f19d74e589f10001945721',
            # '64f19ea11134240001c3054f',
            # "64f1a115eac6c8000139e4a9",
            "64f6f1d68b8054000194ce27",
        ]
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, json=data)

    # print(response.text)

    detailed_result = response.json()["tasks_info"][0]["task_result"]["detailed_result"]
    for item in detailed_result:
        begin_time = item["begin_time"]
        end_time = item["end_time"]
        # 将毫秒时间打印转换为分秒的时间
        print(f'{begin_time // 1000 // 60}:{begin_time // 1000 % 60} - {end_time // 1000 // 60}:{end_time // 1000 % 60}')
        print(item["res"])
        print()


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


if __name__ == '__main__':
    main()
