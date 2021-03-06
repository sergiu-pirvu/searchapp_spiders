from scrapy.spiders import Spider
import re
import scrapy

from spiders.items import EmagItem

class EmagSpider(Spider):

	name            = 'emag'
	filename        = 'emag.txt'

	start_urls = [
		'http://www.emag.ro/all-departments?ref=hdr_mm_14'
	]

	def parse(self, response):
		for item in response.xpath('//div[@id="department-expanded"]/ul/li/ul/li/a/@href'):
			url = response.urljoin(item.extract())
			yield scrapy.Request(url, callback=self.parseList)
						
	def parseList(self, response):
		for item in response.xpath('//a[@class="link_imagine "]/@href'):
			url = response.urljoin(item.extract())
			yield scrapy.Request(url, callback=self.parseDetails)
		next_item = response.xpath('//span[@class="emg-pagination-no emg-pagination-selected"]/following-sibling::a/@href').extract_first()
		if not next_item: 
			return
		
		next_item = response.urljoin(next_item)
		print next_item
		yield scrapy.Request(next_item, callback=self.parseList)
						
	def parseNextPage(item):
		print item
		yield scrapy.Request(item, callback=self.parseList)
		
	def parseDetails(self, response):
		value_int = response.xpath('//span[@class="money-int"]/text()').extract_first().replace(".", "")
		value_decimal = response.xpath('//span[@class="money-int"]/following-sibling::sup/text()').extract_first()
		seller = response.xpath('//div[@class="vendor-name"]/span/text()').extract_first()
		
		if not seller:
			seller = response.xpath('//div[@class="vendor-name"]/a/text()').extract_first()
		
		
		if response.xpath('//span[@class="stock-info-box in_stock"]').extract_first():
			status = 1
		else: 
			status = 0
		
		categories = response.xpath('//span[@itemprop="itemListElement"]/a/span/text()').extract()
				
		item = EmagItem()
		item['title'] = response.xpath('//h1[@class="product-title"]/text()').extract_first().strip()
		item['brand'] = response.xpath('//div[@class="disclaimer-section"]/p/a/text()').extract_first()
		item['price'] = str(value_int) + "." + str(value_decimal)
		item['seller'] = seller
		item['status'] = status
		item['categories'] = categories[1].strip()
		item['description'] = "aaaaaaa"
		yield item
		#item['description'] = response.xpath('//div[@class="description-section"]/div[@class="description-content"]').extract_first()
				
