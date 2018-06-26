# -*- coding: utf-8 -*-
from time import sleep
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


class YelpSpider(Spider):
    name = 'yelp'
    allowed_domains = ['www.yelp.com']

    def __init__(self, description, location):
        self.description = description
        self.location = location

    def start_requests(self):
        self.logger.info('Starging scraping Yelp with description=' +
                         self.description + ', location=' + self.location)

        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # self.driver = webdriver.Chrome(options=options)
        self.driver = webdriver.Chrome()
        self.driver.get('http://www.yelp.com/')

        # Search keywords in a home page
        input_description = self.driver.find_element_by_xpath(
            '//input[@id="find_desc"]')
        input_location = self.driver.find_element_by_xpath(
            '//input[@id="dropperText_Mast"]')

        input_description.send_keys(self.description)
        input_location.clear()
        input_location.send_keys(self.location)
        input_location.send_keys(Keys.RETURN)

        while True:
            try:
                # Scrape a whole page
                sel = Selector(text=self.driver.page_source)
                links = sel.xpath(
                    '//h3[@class="search-result-title"]/span/a/@href').extract()
                for link in links:
                    url = 'https://www.yelp.com' + link
                    yield Request(url, callback=self.parse_link)

                # Go to a next page
                next_page = self.driver.find_element_by_xpath(
                    '//a[contains(@class, "pagination-links_anchor")]/span[text()="Next"]')
                next_page.click()
                sleep(3)
                self.logger.info('Waiting for 3 seconds...')

            except NoSuchElementException:
                self.driver.quit()
                self.logger.info('Finished to scrape Yelp.')
                break

    def parse_link(self, response):
        title = response.xpath(
            '//h1[contains(@class, "biz-page-title")]/text()').extract_first()
        title = title.strip()
        rating = response.xpath(
            '//div[contains(@class, "biz-main-info")]/div/div/div/@title').extract_first()
        rating = rating.replace(' star rating', '')
        rating = rating.strip()
        address_strings = response.xpath(
            '//div[@class="biz-page-subheader"]/div/div/div/ul/li/div/strong/address/text()').extract()
        address = ' '.join(address_strings)
        address = address.strip()

        yield {'title': title, 'rating': rating, 'address': address}
