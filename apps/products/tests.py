from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, ProductDocument, ProductImage


class PublicCatalogApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(name='Natural Plant Fibers', slug='fibers')
        cls.product = Product.objects.create(
            name='Banana fiber', category=category, is_featured=True, moq='500 kg',
            verified_specs={'Length': {'value': '50 cm'}},
            provisional_specs={'Colour': {'value': 'Golden', 'note': 'Supplier estimate'}},
        )
        cls.inactive = Product.objects.create(name='Unpublished material', is_active=False)
        ProductImage.objects.create(product=cls.product, image='products/images/gallery.jpg')
        ProductImage.objects.create(product=cls.product, image='products/images/main.jpg', is_primary=True)
        ProductDocument.objects.create(
            product=cls.product, title='Fiber technical sheet', document_file='products/documents/fiber.pdf',
        )

    def test_list_uses_live_public_records_and_absolute_image_urls(self):
        list_url = reverse('api-product-list')
        storage = ProductImage._meta.get_field('image').storage
        with patch.object(storage, 'url', side_effect=lambda name: '/media/' + name):
            products = self.client.get(list_url, secure=True).json()['products']
            self.assertEqual(len(products), 1)
            self.assertEqual(products[0]['slug'], self.product.slug)
            self.assertTrue(products[0]['is_featured'])
            self.assertEqual(products[0]['image']['url'], 'https://testserver/media/products/images/main.jpg')
            self.product.is_active = False
            self.product.save(update_fields=['is_active'])
            self.assertEqual(self.client.get(list_url, secure=True).json(), {'products': []})

    def test_detail_preserves_storage_urls_and_verification_labels(self):
        cdn = 'https://example.supabase.co/storage/v1/object/public/catalog/'
        storage = ProductImage._meta.get_field('image').storage
        with patch.object(storage, 'url', side_effect=lambda name: cdn + name):
            response = self.client.get(reverse('api-product-detail', args=[self.product.slug]), secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        detail = response.json()
        self.assertEqual([image['url'] for image in detail['gallery']], [
            cdn + 'products/images/gallery.jpg', cdn + 'products/images/main.jpg',
        ])
        self.assertEqual(detail['documents'][0]['url'], cdn + 'products/documents/fiber.pdf')
        self.assertEqual([(spec['name'], spec['is_verified']) for spec in detail['specifications']], [
            ('Length', True), ('Colour', False),
        ])

    def test_hidden_products_return_json_404_and_public_routes_reject_writes(self):
        detail_url = reverse('api-product-detail', args=[self.inactive.slug])
        response = self.client.get(detail_url, secure=True)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response['Content-Type'], 'application/json')
        for url in (detail_url, reverse('api-product-list')):
            self.assertEqual(self.client.post(url, secure=True).status_code, 405)
