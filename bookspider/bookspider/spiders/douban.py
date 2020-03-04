# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib.parse import urljoin
from bookspider.items import BookspiderItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/神经网络']

    def parse(self, response):
        get_nodes = response.xpath('//div[@id="subject_list"]/ul/li/div[@class="pic"]/a')
        for node in get_nodes:
            url = node.xpath("@href").get()
            img_url = node.xpath('img/@src').get()
            yield Request(url=url, meta={"img_url": img_url},
                          callback=self.parse_book)  # 传递img_url值 放在meta里面， parse_book回调函数，获取的详情再分析

        next_url = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').get()  # 获取下一页地址
        if (next_url):
            yield Request(url=urljoin(response.url, next_url), callback=self.parse)  # 获取下一页内容



    def parse_book(self, response):
        BookItem = BookspiderItem()
        BookItem['name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').get("").strip()
        BookItem['author'] = response.xpath('//span[contains(text(), "作者")]/following-sibling::a[1]/text()').get("").split()[-1]
        BookItem['publish'] = response.xpath('//span[contains(text(), "出版社")]/following-sibling::text()').get("").strip()

        page_num = response.xpath('//span[contains(text(), "页数")]/following-sibling::text()').get("").strip()
        BookItem['page_num'] = 0 if (page_num == '') else page_num

        BookItem['isbm'] = response.xpath('//span[contains(text(), "ISBN")]/following-sibling::text()').get("").strip()
        # BookItem['binding'] = response.xpath('//span[contains(text(), "装帧")]/following-sibling::text()').get("").strip()
        # BookItem['publish_date'] = response.xpath('//span[contains(text(), "出版年")]/following-sibling::text()').get(
        #     "").strip()
        #
        # price = response.xpath('//span[contains(text(), "定价")]/following-sibling::text()').get("").strip()
        # BookItem['price'] = '' if (len(price) == 0) else re.findall(r'\d+\.?\d*', price)[0]
        #
        # BookItem['rate'] = response.xpath('//div[contains(@class, "rating_self ")]/strong/text()').get("").strip()
        #
        # BookItem['img_url'] = [response.meta.get('img_url')]  # 图片是列表

        yield BookItem
