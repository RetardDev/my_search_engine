from django.contrib import admin
from .models.web import Site, Webpage, Keyword, KeywordMapping

# Register your models here.
admin.site.register(Site)
admin.site.register(Webpage)
admin.site.register(Keyword)
admin.site.register(KeywordMapping)


