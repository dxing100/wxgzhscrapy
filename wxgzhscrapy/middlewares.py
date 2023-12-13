# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import time
from random import random, randint

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from scrapy.http import HtmlResponse


class WxgzhscrapySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class WxgzhscrapyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if spider.debug and self.read_file() is not None:
            html_content = self.read_file()
            return HtmlResponse(url=request.url, body=html_content, encoding='utf8',
                                request=request)
        else:
            spider.driver.get(request.url)
            # last_height = spider.driver.execute_script("return document.body.scrollHeight")
            #
            # # 模拟下拉操作，直到滑动到底部
            # while True:
            #     # 模拟下拉操作
            #     spider.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #     # 等待页面加载 随机1～5s
            #     time.sleep(randint(1, 5))
            #     # 获取当前页面的高度
            #     new_height = spider.driver.execute_script("return document.body.scrollHeight")
            #     # 判断是否已经到达页面底部
            #     if new_height == last_height:
            #         break
            #     # 继续下拉操作
            #     last_height = new_height
            # 写入测试html数据
            self.write_file(spider.driver.page_source)

        return HtmlResponse(url=spider.driver.current_url, body=spider.driver.page_source, encoding='utf8',
                            request=request)

    def process_response(self, request, response, spider):
        # if spider.name == 'wxgzhspider':
        #     li_size = 0
        #     def_size = 0
        #     while li_size != def_size & li_size != 0:
        #         li = response.xpath('//div[@class="album__list js_album_list"]/li')
        #         li_size = len(li)
        #         spider.browser.get(request.url)
        #         spider.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # return response
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


    def read_file(self):
        html = ''
        if not os.path.exists('debug.html'):
            return None
        with open('debug.html', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                html.join(line)
        return html


    def write_file(self, body):
        with open('debug.html', 'w', encoding='utf-8') as file:
            file.write(body)
        return str
