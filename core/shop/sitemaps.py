from django.contrib import sitemaps
from django.urls import reverse
from .models import Product , ProductStatus

class productsitemap(sitemaps.Sitemap):
    priority= 1.0 
    changefreq = "daily"
    def items(self):
        return Product.objects.filter(status=ProductStatus.publish.value)
    def lastmod(self,obj):
        return obj.updated_date
    def location(self, item):
        return reverse('shop:products-detail',kwargs={'slug':item.slug})