import time

import scrapy
from pydispatch import dispatcher
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver

from wxgzhscrapy.items import WxgzhscrapyItem


class WxgzhspiderSpider(scrapy.Spider):
    name = "wxgzhspider"
    allowed_domains = ["mp.weixin.qq.com"]
    start_urls = ['https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzU5NjcwODg0MA==&action=getalbum&album_id'
                  '=1808531910277545984&scene=173&from_msgid=2247495991&from_itemidx=1&count=3&nolastread=1'
                  '#wechat_redirect']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.debug = False
        option = webdriver.ChromeOptions()  # 实例化一个浏览器对象
        option.add_argument('--headless')  # 添加参数，option可以是headless，--headless，-headless
        option.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=option)  # 创建一个无头浏览器
        dispatcher.connect(self.close_driver, signals.spider_closed)

    def parse(self, response: HtmlResponse, *args, **kwargs):
        lis = response.xpath("//ul[@class='album__list js_album_list']/li")
        item = WxgzhscrapyItem
        for li in lis:
            item['title'] = li.get('data-title')
            item['time'] = li.xpath(".//span[@class='js_article_create_time album__item-info-item']/text()").get()
        time.sleep(3)
        dispatcher.connect(self.close_driver, signals.spider_closed)

    def close_driver(self):
        print("爬虫正在退出，执行关闭浏览器哦")
        time.sleep(2)
        self.driver.quit()
