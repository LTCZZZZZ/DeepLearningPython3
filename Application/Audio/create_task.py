# 百度智能云-语音识别-长语音识别-创建识别任务
# 识别较长的英文语音
import os, sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
import requests
import json
from tools.connection import config_dict

baidu_config = config_dict('baidu')
API_KEY = baidu_config['API_KEY']
SECRET_KEY = baidu_config['SECRET_KEY']
print(API_KEY)
print(SECRET_KEY)


# 将原音频文件转为采样率=16000的wav格式文件
# ffmpeg -i XXX.mp3 -ac 1 -ar 16000 -sample_fmt s16 output.wav


def main():
    url = "https://aip.baidubce.com/rpc/2.0/aasr/v1/create?access_token=" + get_access_token()

    payload = json.dumps({
        # "speech_url": "https://afp-71129-injected.calisto.simplecastaudio.com/6fa1d34c-502b-4abf-bd82-483804006e0b/episodes/cc66017d-f764-4ea3-a673-019ed17f9c2d/audio/128/default.mp3/default.mp3_ywr3ahjkcgo_2269d1e0ae1d6a484e7b63ed2118b507_21755417.mp3",
        "speech_url": "https://i-beijing.kelexuexi.com/m/20230905/0/6a3d6f22c8415cc4d31f3e2251502239e4c9d939",
        "format": "pcm",
        "pid": 1737,
        "rate": 16000
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


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
