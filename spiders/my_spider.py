import scrapy
from urllib.parse import urlparse, urljoin
from search_engine.models.web import Site, Webpage
import django
import os

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_search_engine.settings')
django.setup()

class MySpider(scrapy.Spider):
    name = 'myspider'

    def start_requests(self):
        # Fetch main sites from the Sites table
        main_sites = Site.objects.all()
        
        for main_site in main_sites:
            url = self.ensure_scheme(main_site.url)
            yield scrapy.Request(url=url, callback=self.parse, errback=self.errback, meta={'main_site': main_site})

    def ensure_scheme(self, url):
        """Ensure the URL has a scheme (http or https)."""
        parsed_url = urlparse(url)
        if not parsed_url.scheme:
            return 'http://' + url
        return url

    def parse(self, response):
        main_site = response.meta.get('main_site')

        # Extract URLs
        urls = response.css('a::attr(href)').getall()
        
        for url in urls:
            # Handle relative URLs
            absolute_url = urljoin(response.url, url)
            
            # Ensure the URL has a scheme
            absolute_url = self.ensure_scheme(absolute_url)
            
            # Save subsite
            webpage, created = Webpage.objects.get_or_create(
                site=main_site,
                url=absolute_url,
                defaults={'title': '', 'content': ''}
            )
            
            yield {'url': absolute_url}

            # Optionally, follow links to scrape more pages
            yield scrapy.Request(url=absolute_url, callback=self.parse_subpage, errback=self.errback, meta={'main_site': main_site})

    def parse_subpage(self, response):
        main_site = response.meta.get('main_site')

        # Extract title and content from the subpage
        title = response.css('title::text').get(default='')
        content = ' '.join(response.css('body *::text').getall()).strip()

        # Save/update the subsite with title and content
        webpage, created = Webpage.objects.update_or_create(
            site=main_site,
            url=response.url,
            defaults={'title': title, 'content': content},
        )
        
        yield {
            'url': response.url,
            'title': title,
            'content': content
        }

    def errback(self, failure):
        self.logger.error(repr(failure))
        # This will continue the crawling process by ignoring the failed request
        pass
