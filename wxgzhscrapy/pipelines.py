# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class WxgzhscrapyPipeline:
    def process_item(self, item, spider):
        # 将型号数据存储到CSV文件中
        name = 'wxgzh_spider.csv'
        with open(name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([item['title'], item['time']])
        return item
