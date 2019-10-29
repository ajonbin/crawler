# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from urllib.parse import parse_qs
from icanread.items import IcanreadItem

class IcanreadSpiderSpider(scrapy.Spider):
    name = 'icanread_spider'
    allowed_domains = ['icanread.com']
    start_urls = ['https://www.icanread.com/levels/']
    
    def parse(self, response):
        level_urls = response.xpath('//a[@class="button-rounded"]/@href').extract()
        level_titles = response.xpath('//a[@class="button-rounded"]/text()').extract()

        levels = dict(zip(level_titles, level_urls)) 
        levels = {k.replace("see all I can Read! ",""):v for k,v in levels.items()} 

        for title, url in levels.items():
            level_page_url = response.urljoin(url) + "&page_number=1"
            yield scrapy.Request(level_page_url, callback=self.parse_level_list)

    def parse_level_list(self, response):
        url_parsed = urlparse(response.url)

        book_level = parse_qs(url_parsed.query)['series'][0]
        page_number = int(parse_qs(url_parsed.query)['page_number'][0])
        next_page = page_number + 1

        try:
            books = response.xpath('//div[@class="book-wrapper left"]')
            if len(books) == 0:
                return
            
            for book in books:
                book_item = IcanreadItem()
                book_item['level'] = book_level
                book_item['character'] = ""
                book_item['image'] = book.xpath('.//img/@src').extract_first()
                book_item['title'] = book.xpath('.//p[@class="sp__the-title"]/text()').extract_first()
                book_item['format'] = book.xpath('.//p[@class="sp__the-format"]/text()').extract_first()
                yield book_item

            next_page_url = response.url.replace("page_number=%d"%page_number, "page_number=%d"%next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_level_list)

        except Exception as e:
            self.logger.error(e)
