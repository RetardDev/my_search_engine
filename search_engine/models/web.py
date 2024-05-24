from django.db import models

class Site(models.Model):
    url = models.URLField(unique=True)

    def __str__(self):
        return self.url

class Webpage(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    url = models.URLField(unique=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Keyword(models.Model):
    keyword = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.keyword

class KeywordMapping(models.Model):
    webpage = models.ForeignKey(Webpage, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    frequency = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('webpage', 'keyword')

    def __str__(self):
        return f'{self.webpage} - {self.keyword}'