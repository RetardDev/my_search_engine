#get webpages from the webpage model 
#get their contents, use nltk to tokenise it and remove stop words
#add keywords from the gathered webpage into the keyword table and then keyword mapping

import scrapy 
from search_engine.models.web import Site, Webpage, Keyword, KeywordMapping
import django
import os 
from django.shortcuts import get_object_or_404
import html2text
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from urllib.parse import urlparse, urljoin

os.environ['DJANGO_SETTINGS_MODULE'] = 'my_search_engine.settings'
django.setup()

import nltk
nltk.download('punkt')
nltk.download('stopwords')

class MyKeySpider(scrapy.Spider):
    name = "myspider"

    def start_requests(self):
        # page = Webpage.objects.last()
        # url = page.url
      
        # yield scrapy.Request(url=url, callback=self.parse)
        webpages = Webpage.objects.all()
        for page in webpages:
            url = page.url
            domain = urlparse(url).netloc
            self.allowed_domains = [domain]
            yield scrapy.Request(url=url, callback=self.parse, cb_kwargs={'webpage_id' : page.id})

    def parse(self, response):
        content = response.body.decode('utf-8')
        textconv = html2text.HTML2Text()   
        textconv.ignore_links = True
        text_content = textconv.handle(content)

        text_content = re.sub(r'\n+', '\n', text_content)
        text_content = re.sub(r'\s+', ' ', text_content)
        text_content = text_content.strip()

        #tokenise and remove stop words
        tokens = word_tokenize(text_content)
        stop_words = set(stopwords('english'))
        filtered_tokens = [word for word in tokens if word.isalnum() and word.lower() not in stop_words]
        filtered_tokens = [word.lower() for words in filtered_tokens]
        keyword_count = Counter(filtered_tokens)

        webpage = get_object_or_404(Webpage, id=webpage_id)

        for word, fequency in keyword_count.items():
            keyword, created = Keyword.objects.get_or_create(word=word)
            keyword_mapping, created = KeywordMapping.objects.get_or_create(webpage=webpage, keyword=keyword)
            if not created:
                keyword_mapping.frequency += frequency
            else:
                keyword_mapping.frequency = frequency
            keyword_mapping.save()

        yield{'webpage_id' : webpage_id,
                'keywords': keyword_count}