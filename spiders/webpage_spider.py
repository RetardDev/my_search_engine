import scrapy
from urllib.parse import urlparse, urljoin

from search_engine.models.web import Site, Webpage
import django
import os
import sys 

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_search_engine.settings'
django.setup()


class MyWebpageCrawler(scrapy.Spider):
    name = "myspider"

    def start_requests(self):
        sites = Site.objects.all()
        for site in sites:
            url = site.url
            domain = urlparse(url).netloc
            self.allowed_domains = [domain]
            yield scrapy.Request(url=url, callback=self.parse, errback=self.errback, meta={'main_site': site})

    def parse(self, response):
        main_site = response.meta.get('main_site')

        links = response.css('a::attr(href)').getall()

        for link in links:
            url = urljoin(response.url, link)

            webpage, created = Webpage.objects.get_or_create(
                site=main_site,
                url=url,
                defaults={'title':'', 'content': ''}
            )
            yield {'url' : url}

            yield scrapy.Request(url=url, callback=self.parse_subpage, errback=self.errback, meta={'main_site': main_site})
    
    def parse_subpage(self, response):
        main_site = response.meta.get('main_site')

        title = response.css('title::text').get(default='')
        
        if not title:
            return

        webpage,created = Webpage.objects.update_or_create(
            site=main_site,
            url=response.url,
            defaults={'title': title, 'content': ''},
        )
        yield {
            'url': response.url,
            'title': title,
        }

    def errback(self, failure):
        pass
