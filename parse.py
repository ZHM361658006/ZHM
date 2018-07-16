import requests
from retrying import retry


#headers ={ "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5514.400 QQBrowser/10.1.1660.400"}
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5514.400 QQBrowser/10.1.1660.400",
         "Referer": "https: // movie.douban.com / tag /"}
@retry(stop_max_attempt_number=3)#让被装饰的函数反复执行3此，3此全部报错才会报错，中间有一次正常，程序继续往后走
def _parse_url(url):
    print("*"*100)
    response = requests.get(url,headers=headers,timeout=5)
    return  response.content.decode()
def parse_url(url):
    try:
        html_str = _parse_url(url) 
    except:
        html_str = None
    return html_str
if __name__== '__main_':
    url = "http://www.baidu.com"
    url1 ="www.baidu.com"
    print(parse_url(url1))