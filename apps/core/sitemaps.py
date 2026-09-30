from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from apps.products.models import Product

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'pages:home',
            'pages:about',
            'pages:quality_process',
            'pages:services',
            'pages:contact',
            'pages:faq',
            'pages:privacy',
            'pages:terms',
            'products:list',
            'rfq:submit',
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return Product.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at
