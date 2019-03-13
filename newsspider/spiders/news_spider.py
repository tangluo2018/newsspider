import scrapy
from newsspider.items import NewsItem


class NewsSpider(scrapy.Spider):
    name = "news"

    def start_requests(self):
        urls = ['https://www.163.com',]
	for url in urls:
	    yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print '''parse response'''
        for news in response.xpath('//div[@class="yaowen_news"]/div/ul/li/a/@href').extract():
	    print news
	    yield scrapy.Request(news, callback=self.parse_news )
            
	    
    def parse_news(self, response):
        for item in response.xpath('//div[@id="epContentLeft"]'):
	    news = NewsItem()
	    news['title'] = item.xpath('h1/text()').extract()[0]
            date_info = item.xpath('div[@class="post_time_source"]/text()').extract()[0]
	    news['author'] = item.xpath('div[@class="post_time_source"]/a[@id="ne_article_source"]/text()').extract()[0]
	    news['date'] = date_info.strip()[0:19]
	    #news['content'] = item.xpath('//div[@class="post_text"]/p/text()').extract()
	    news['content'] = item.xpath('string(//div[@class="post_text"])').extract()
	    yield news
