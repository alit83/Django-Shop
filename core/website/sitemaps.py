from django.contrib import sitemaps
from django.urls import reverse



class staticviewsitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'
    
    def items(self):
        return ['website:contact','website:index' , 'website:about']
    
    def location(self, item):
        return reverse(item)