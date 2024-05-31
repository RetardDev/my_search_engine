from django.contrib import admin
from .models.web import Site, Webpage, Keyword, KeywordMapping
from django.contrib.auth.models import Permission

admin.site.register(Permission)
# Register your models here.
admin.site.register(Site)
admin.site.register(Webpage)
admin.site.register(Keyword)
admin.site.register(KeywordMapping)


