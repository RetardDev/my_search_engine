import scrapy
from urllib.parse import urlparse, urljoin
from search_engine.models.web import Site, Webpage
import django
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_search_engine.settings')
django.setup()

class MySiteCrawler(scrapy.Spider):
    name="myspider"

    def start_requests(self):
        file_txt = r'C:\Users\ataki\OneDrive\Desktop\Intelligent Search Engine\my_search_engine\top-1000-websites.txt'

        with open(file_txt, 'r') as file:
            lines = file.readlines()

        for line in lines:
            web_protocol = 'http://www.'
            correct_url = web_protocol + line.strip()
            yield scrapy.Request(url=correct_url, callback=self.parse, errback=self.errback)
            

    def parse(self, response):
        title = response.css('title::text').get()

        if not title:
            pass

        site, created = Site.objects.get_or_create(
            url=response.url,
            defaults={'title': title},
        )
        if created:
            self.log(f"Site created: {site.url} with title {title}")
        else:
            self.log(f"Site already exists: {site.url}")
    
    def errback(self, failure):
        pass