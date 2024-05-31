from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from ..models.web import KeywordMapping,Keyword, Site, Webpage
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from datetime import datetime
import numpy as np
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer

class Search(View):
    @staticmethod
    def cosine_similarity(A, B):
        A = np.array(A)
        B = np.array(B)
        return np.dot(A, B) / (norm(A)* norm(B))

    @staticmethod
    def log_search(ip_address, query):
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp}, IP: {ip_address}, QUERY: {query}\n"
        with open('Logs.txt', 'a') as logFile:
            logFile.write(log_entry)


    def get(self, request):
        user_request = request.GET.get('search', '')
        tokens = word_tokenize(user_request.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.isalnum() and word.lower() not in stop_words]

        if user_request:
            ip_address = request.META.get('REMOTE_ADDR')
            self.log_search(ip_address, user_request)

        keyword_mappings = []
        site_list = []
        sites = Site.objects.all()

        site_urls = [site.url for site in sites]
        vectoriser = TfidfVectorizer()
        tfidf_matrix = vectoriser.fit_transform(site_urls)

        for token in filtered_tokens:
            if token in vectoriser.vocabulary_:
                token_index = vectoriser.vocabulary_[token]
                token_vector = np.zeros(len(vectoriser.vocabulary_))
                token_vector[token_index] = 1

                for i, site in enumerate(sites):
                    site_vector = tfidf_matrix[i, :].toarray().flatten()
                    cosine = self.cosine_similarity(token_vector, site_vector)

                    if cosine > 0.2:
                        print(site)
                        site_list.append(site.url)

        webpages = Webpage.objects.all()
        webpages_url = [webpage.url for webpage in webpages]

        tfidf_matrix2 = vectoriser.fit_transform(webpages_url)

        for token in filtered_tokens:
            if token in vectoriser.vocabulary_:
                token_index = vectoriser.vocabulary_[token]
                token_vector = np.zeros(len(vectoriser.vocabulary_))
                token_vector[token_index] = 1

                for i, site in enumerate(webpages):
                    site_vector = tfidf_matrix2[i, :].toarray().flatten()
                    cosine = self.cosine_similarity(token_vector, site_vector)

                    if cosine > 0.2:
                        site_list.append(site)


        for token in filtered_tokens:
            matching_keywords = Keyword.objects.filter(keyword__iexact=token)

            for keyword in matching_keywords:
                mappings = KeywordMapping.objects.filter(keyword=keyword)
                
                for mapping in mappings:
                    print(mapping.webpage.title)
                    keyword_mappings.append(mapping.webpage)

        return render(request, 'search.html', {'webpages' : keyword_mappings, 'sites' : site_list, 'query' : user_request})

