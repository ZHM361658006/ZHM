from lxml import etree
import requests
import json



class QiubaiSpider:

    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5514.400 QQBrowser/10.1.1660.400"}

    def get_url_list(self):#根据url地址的规律，构造url list
        url_list= [self.url_temp.format(i)for i in range(1,14)]
        return url_list

    def parse_url(self,url):
        print("now parseing :",url)
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_content_list(self,html_str):#3.提取数据
        html = etree.HTML(html_str)
        #1.分组
        div_list = html.xpath("//div[@id='content-left']/div")
        print(div_list)
        content_list = []
        for div in div_list:
            item = {}
            item["author_name"]= div.xpath(".//h2/text()")[0].strip() if len(div.xpath(".//h2/text()"))>0 else None
            item["content"] = div.xpath(".//div[@class='content']/span/text()")
            item["content"] = [i.strip() for i in item["content"]]
            item["stats_vote"]=div.xpath(".//span[@class='stats-vote']/i/text()")
            item["stats_vote"]=item["stats_vote"][0] if len(item["stats_vote"])>0 else None
            item["stats_comments"]=div.xpath(".//span@class='stats-comments']//i/text()")
            item["stats_comments"] = item["stats_comments"][0] if len(item["stats_comments"])>0 else None
            item["img"] =div.xpath(".//div[@class='thumb']//img/@src")
            item["img"] = "http:"+item["img"][0] if len(item["img"])>0 else None
            content_list.append(item)

        return content_list

    def save_content_list(self,content_list):#保存
        with open("qiubai.txt","a",encoding="utf-8") as f:
            for content in content_list:
                f.write(json.dumps(content,ensure_ascii=False))
                f.write("\n")
        print("保存成功")
    def run(self):# 实现主要逻辑
        #1.根据url地址的规律，构造url list
        url_list = self.get_url_list()
        #2.发送请求,获取响应
        for url in url_list:
            html_str = self.parse_url(url)
        #3.提取数据
            content_list = self.get_content_list(html_str)
        #4.保存
            self.save_content_list(content_list)
if __name__ == '__main__':
    qiubai = QiubaiSpider()
    qiubai.run()
