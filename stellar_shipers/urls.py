from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.core.sitemaps import StaticViewSitemap, ProductSitemap

# Customize Django Admin Header and Titles
admin.site.site_header = "STELLAR SHIPERS | Global Sourcing & Export Operations"
admin.site.site_title = "STELLAR SHIPERS Portal"
admin.site.index_title = "Enterprise Supply Chain & RFQ Pipeline Desk"

sitemaps = {
    'static': StaticViewSitemap,
    'products': ProductSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('rfq/', include('apps.rfq.urls', namespace='rfq')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('apps.pages.urls', namespace='pages')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
