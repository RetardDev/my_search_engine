from django.contrib import admin
from .models.web import Site, Webpage

# Register your models here.
admin.site.register(Site)
admin.site.register(Webpage)


