import os
import django
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_search_engine.settings')
django.setup()

from spiders.myspider import MyspiderSpider  # Import your spider after setting up Django

def run_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl(MyspiderSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
