from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.template import loader
from django.views import View
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from ..models.web import KeywordMapping,Keyword, Site
import nltk
nltk.download('punkt')
nltk.download('stopwords')

import numpy as np
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer
import logging

logger = logging.getLogger(__name__)
class Search(View):
    @staticmethod
    def cosine_similarity(A, B):
        A = np.array(A)
        B = np.array(B)
        return np.dot(A, B) / (norm(A)* norm(B))

    def get(self, request):
        user_request = request.GET.get('search', '')
        tokens = word_tokenize(user_request.lower())
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.isalnum() and word.lower() not in stop_words]

        # keywordMap = KeywordMapping.objects.filter(keyword__keyword__in=filtered_tokens).select_related('webpage')
        # webpages = list(set([km.webpage.url for km in keywordMap]))
        
        

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

                    if cosine > 0.5:
                        site_list.append(site.url)

        for token in filtered_tokens:
            matching_keywords = Keyword.objects.filter(keyword=token)

            for keyword in matching_keywords:
                mappings = KeywordMapping.objects.filter(keyword=keyword)
                
                for mapping in mappings:
                    print(mapping.webpage.title)
                    keyword_mappings.append(mapping.webpage)

        return render(request, 'search.html', {'webpages' : keyword_mappings, 'sites' : site_list})

    
        # return render(request, 'search.html', {'webpages' : webpages})