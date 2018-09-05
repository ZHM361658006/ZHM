# coding=utf-8
import requests
from lxml import etree
import json
import pymysql

item = {}
class DoubanSpider:

    def __init__(self):
        self.url_temp = "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T"
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400",
                        "Referer": "https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4?start={}&type=T/"}

    def get_url_list(self): #根据url地址的规律,构造url list
        url_list = [self.url_temp.format(i) for i in range(0,1000,20)]
        return url_list

    def parse_url(self,url):
        print("now parseing :",url)
        response = requests.get(url,headers=self.headers)
        return response.content.decode()

    def get_content_list(self,html_str):#3.提取数据
        html = etree.HTML(html_str)
        #1.分组
        div_list = html.xpath("//div[@id='subject_list']/ul/li")
        #print(div_list)
        content_list = []
        for div in div_list:

            item["bookname"] = div.xpath("normalize-space(.//h2/a/text())")
            item["author"] = div.xpath("normalize-space(.//div[@class='pub']/text())")
            item["rating_nums"] = div.xpath("normalize-space(.//span[@class='rating_nums']/text())")
            item["pl"] = div.xpath("normalize-space(.//span[@class='pl']/text())")
            item["content"] = div.xpath(".//p/text()")
            item["content"] = [i.strip() for i in item["content"]]
            item["img"] = div.xpath(".//div[@class='pic']//img/@src")
            item["img"] = "https:"+item["img"][0] if len(item["img"])>0 else None
            content_list.append(item)
            print((content_list))
        return content_list

    def save_content_list(self,content_list):# 保存
        with open("doubannew1.txt","a",encoding="utf-8") as f:
            for content in content_list:
                print(content)
                f.write(json.dumps(content, ensure_ascii=False))
                f.write("\n")
        print("保存成功")


    def run(self):#实现主要逻辑
        #1.根据url地址的规律,构造url list
        url_list = self.get_url_list()
        #2.发送请求,获取响应
        for url in url_list:
            html_str = self.parse_url(url)
            #3.提取数据
            content_list = self.get_content_list(html_str)
            #4.保存
            self.save_content_list(content_list)

    def sql(self):
        conn = pymysql.connect(host='localhost', user='root', password='', port=3306, db='ZZZ')
        cursor = conn.cursor()
        sql = "insert into book values(%s,%s)"

        bookname = item["bookname"]
        autor = item["author"].extract().split('/')[0]
        content = item["content"].extract()
        rating_num = item["rating_num"].extract()
        values = (bookname, autor, content, rating_num)
        cursor.execute(sql, values)
        conn.commit()


if __name__ == '__main__':
    douban = DoubanSpider()
    douban.run()
    douban.sql()
