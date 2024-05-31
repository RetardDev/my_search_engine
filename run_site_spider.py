import os
import django
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_search_engine.settings')
django.setup()

from spiders.site_spider import MySiteCrawler

def run_crawler():
    process  = CrawlerProcess(get_project_settings())
    process.crawl(MySiteCrawler)
    process.start()

if __name__ == "__main__":
    run_crawler()