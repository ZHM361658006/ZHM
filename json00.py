import requests
import json

url = "http://fanyi.baidu.com/basetrans"
query_str = input("请输入要翻译的中文")
data = {
    "from": "zh",
    "to": "en",
    "query": query_str
}
headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1",
    "Referer": "http://fanyi.baidu.com/?aldtype=16047"
    }
response = requests.post(url, data=data, headers=headers)
html_str = response.content.decode()  #json字符串
dict_ret = json.loads(html_str)
print(dict_ret)

ret = dict_ret["trans"][0]["dst"]
print("翻译结果是",ret)