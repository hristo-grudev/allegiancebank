import scrapy

from scrapy.loader import ItemLoader

from ..items import AllegiancebankItem
from itemloaders.processors import TakeFirst


class AllegiancebankSpider(scrapy.Spider):
	name = 'allegiancebank'
	start_urls = ['https://allegiancebank.com/resources/news-insights/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="fl-post-more-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="fl-archive-nav-next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h1/span[@class="fl-heading-text"]/text()').get()
		description = response.xpath('//div[@class="fl-module fl-module-fl-post-content fl-node-59db14bd25310"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=AllegiancebankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
