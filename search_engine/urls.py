from django.urls import path, include, re_path
from .views.home import Index
from .views.search import Search

from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('', Index.as_view(), name='Home'),
    path('search', Search.as_view(), name='Search')
]
