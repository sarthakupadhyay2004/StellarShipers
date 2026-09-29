from django.test import TestCase, Client
from django.urls import reverse
from apps.products.models import Product, Category
from apps.rfq.models import RFQ

class StellarShiperHandoffComplianceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Natural Plant Fibers', slug='natural-plant-fibers')
        self.product = Product.objects.create(
            category=self.category,
            name='Textile-grade raw banana fiber',
            slug='banana-fiber',
            raw_material='Musa plant pseudostems (G9 Grand Naine)',
            extraction_method='Mechanical decortication',
            processing='Drying only',
            harvest_origin='Jalgaon, Maharashtra, India',
            moq='500 kg',
            verified_specs={},
            provisional_specs={
                'Banana Variety': {'value': 'G9 (Grand Naine)', 'note': 'Supplier-stated'},
                'Extraction': {'value': 'Mechanical', 'note': 'Confirmed'}
            },
            is_active=True,
            is_featured=True
        )

    def test_all_10_core_pages_http_200(self):
        pages = [
            ('pages:home', {}),
            ('pages:about', {}),
            ('products:list', {}),
            ('products:detail', {'slug': self.product.slug}),
            ('pages:quality_process', {}),
            ('pages:contact', {}),
            ('pages:faq', {}),
            ('pages:privacy', {}),
            ('pages:terms', {}),
            ('pages:robots', {}),
        ]
        for url_name, kwargs in pages:
            url = reverse(url_name, kwargs=kwargs)
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Page {url} failed with status {response.status_code}")

    def test_homepage_handoff_content_and_positioning(self):
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)
        # Headline & supporting line
        self.assertContains(response, 'WHERE TRUST')
        self.assertContains(response, 'MEETS VALUE.')
        self.assertContains(response, 'Indian sourcing. International standards. Responsible export coordination.')
        # 6-Stage Process
        self.assertContains(response, 'Carefully selected sourcing network')
        self.assertContains(response, 'Requirement-led sourcing')
        self.assertContains(response, 'Quality verification before export')
        # Assert removed sections are no longer on homepage
        self.assertNotContains(response, 'Brand Foundations')
        self.assertNotContains(response, 'Positioning & Transparency')

    def test_specification_integrity_rules(self):
        response = self.client.get(reverse('products:detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Textile-grade raw banana fiber')
        self.assertContains(response, 'Musa plant pseudostems')
        self.assertContains(response, 'Mechanical decortication')
        self.assertContains(response, 'test-measured per buyer specification')

    def test_rfq_submission_creates_record(self):
        data = {
            'name': 'Antoine Dubois',
            'company': 'Alsace Textile SA',
            'country': 'France',
            'email': 'a.dubois@alsacetextile.fr',
            'phone': '+33 3 88 12 34 56',
            'product': self.product.id,
            'quantity': '1000 kg trial lot',
            'application': 'Blended cotton-banana yarn development',
            'technical_requirements': 'Clean combed fiber bundles, 4-5 ft length',
            'packaging': 'Polythene export bags',
            'delivery_country': 'Port of Le Havre, France',
            'incoterms': 'CIF',
            'message': 'Sample evaluation lot needed for spinning trial.',
            'sample_request': True,
            'consent': True,
            'website_check': ''
        }
        response = self.client.post(reverse('rfq:submit'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('rfq:success'))
        
        rfq = RFQ.objects.filter(email='a.dubois@alsacetextile.fr').first()
        self.assertIsNotNone(rfq)
        self.assertTrue(rfq.sample_request)
        self.assertEqual(rfq.status, 'NEW')

    def test_contact_form_submission_with_single_country_auto_sync(self):
        # Scenario where user fills delivery_country only (as was in contact form)
        data = {
            'name': 'Hans Schmidt',
            'company': 'Bavaria Yarns GmbH',
            'email': 'schmidt@bavariayarns.de',
            'delivery_country': 'Germany',
            'quantity': '500 kg',
            'application': 'Textile spinning',
            'consent': True,
            'source_page': 'contact',
            'website_check': ''
        }
        response = self.client.post(reverse('rfq:submit'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('rfq:success'))

        rfq = RFQ.objects.filter(email='schmidt@bavariayarns.de').first()
        self.assertIsNotNone(rfq)
        self.assertEqual(rfq.country, 'Germany')
        self.assertEqual(rfq.delivery_country, 'Germany')

    def test_contact_form_invalid_stays_on_contact_page(self):
        # Missing required fields from contact page should stay on contact page
        data = {
            'name': 'Hans Schmidt',
            'source_page': 'contact',
            'website_check': ''
        }
        response = self.client.post(reverse('rfq:submit'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/contact_rfq.html')
        self.assertContains(response, 'Please correct the highlighted errors')

    def test_contact_form_submission_with_buyer_country_auto_sync(self):
        # Scenario where user fills country only
        data = {
            'name': 'Klaus Weber',
            'company': 'Stuttgart Fibers KG',
            'email': 'klaus@stuttgartfibers.de',
            'country': 'Germany',
            'quantity': '20 MT',
            'application': 'Automotive door trim',
            'consent': True,
            'source_page': 'contact',
            'website_check': ''
        }
        response = self.client.post(reverse('rfq:submit'), data=data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('rfq:success'))

        rfq = RFQ.objects.filter(email='klaus@stuttgartfibers.de').first()
        self.assertIsNotNone(rfq)
        self.assertEqual(rfq.country, 'Germany')
        self.assertEqual(rfq.delivery_country, 'Germany')
        self.assertEqual(rfq.incoterms, 'CIF')

    def test_light_theme_structure_and_navbar_toggle(self):
        response = self.client.get(reverse('pages:home'))
        self.assertEqual(response.status_code, 200)
        # Theme toggle present in navbar
        self.assertContains(response, 'theme-toggle-btn')
        self.assertContains(response, 'theme-opt-light')
        self.assertContains(response, 'theme-opt-dark')
        # Navbar and Footer stay dark
        self.assertContains(response, 'bg-[#1E2328]/95')
        self.assertContains(response, 'bg-[#181C21]')
        # Body default has light background with dark variant
        self.assertContains(response, 'bg-white')
        self.assertContains(response, 'dark:bg-[#0B0F17]')
        # Theme dot indicator present
        self.assertContains(response, 'theme-dot')

