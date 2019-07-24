import requests
import re
import json


class WechatSprot(object):
    def __init__(self, openid):
        self.openid = openid

    def getInfo(self):
        url = "http://hw.weixin.qq.com/steprank/step/personal"

        querystring = {"openid": self.openid}

        headers = {
            'host': "hw.weixin.qq.com",
            'connection': "keep-alive",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400",
            'accept-encoding': "gzip, deflate",
            'accept-language': "zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4",
            'cookie': "hwstepranksk=JxMBWw1sxQhxnMgsJnnLh-r0VFzLH6RtJWv5b_j3z8MPs6-J; pass_ticket=p9R%2FqjIh%2BlXt%2BoxP7GIWrqm3Sbf1Minisk%2FNUz5zra4ReETR2ATI8H57zkEERCvG",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        res = re.findall('window.json = (.+);', response.text)
        print(res)
        exit()
        return json.loads(res[0])


if __name__ == "__main__":
    obj = WechatSprot('ll382640782')
    print(obj.getInfo())