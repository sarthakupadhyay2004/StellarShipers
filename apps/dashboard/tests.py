import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.rfq.models import RFQ
from apps.products.models import Product, Category
from apps.pages.models import FAQ

class DashboardSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='staff_test',
            password='Password123!',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='buyer_test',
            password='Password123!',
            is_staff=False
        )
        self.cat = Category.objects.create(name='Natural Fibers', slug='natural-fibers')
        self.product = Product.objects.create(
            name='Test Banana Fiber',
            slug='test-banana-fiber',
            category=self.cat,
            raw_material='Banana Pseudostem',
            extraction_method='Mechanical',
            processing='Cleaned',
            provisional_specs={'Moisture': {'value': '10-12%', 'note': 'Test note'}},
            verified_specs={'Tensile Strength': {'value': 'Per spec', 'note': 'Lab test'}}
        )
        self.rfq = RFQ.objects.create(
            reference_id='STELLAR-2026-TEST',
            name='John Doe',
            email='john@buyer.com',
            company='Buyer Corp',
            country='Germany',
            product=self.product,
            quantity='5 MT',
            status='NEW'
        )
        self.faq = FAQ.objects.create(
            category='SOURCING',
            question='What do you supply?',
            answer='Natural banana fiber.',
            display_order=1
        )

    def test_anonymous_redirect_to_login(self):
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/dashboard/login/', response.url)

    def test_non_staff_forbidden(self):
        self.client.login(username='buyer_test', password='Password123!')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, 'dashboard/403.html')

    def test_staff_access_overview(self):
        self.client.login(username='staff_test', password='Password123!')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'STELLAR-2026-TEST')
        self.assertContains(response, 'Buyer Corp')

    def test_staff_rfq_list_and_filter(self):
        self.client.login(username='staff_test', password='Password123!')
        response = self.client.get(reverse('dashboard:rfq_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'STELLAR-2026-TEST')

        # Filter by query
        resp_filter = self.client.get(reverse('dashboard:rfq_list') + '?q=Buyer')
        self.assertEqual(resp_filter.status_code, 200)
        self.assertContains(resp_filter, 'STELLAR-2026-TEST')

        resp_miss = self.client.get(reverse('dashboard:rfq_list') + '?q=NonExistent')
        self.assertEqual(resp_miss.status_code, 200)
        self.assertNotContains(resp_miss, 'STELLAR-2026-TEST')

    def test_staff_rfq_status_update(self):
        self.client.login(username='staff_test', password='Password123!')
        response = self.client.post(
            reverse('dashboard:rfq_detail', kwargs={'pk': self.rfq.pk}),
            {
                'status': 'REVIEWING',
                'admin_notes': 'Allocated to Tamil Nadu supplier for sample testing.'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.rfq.refresh_from_db()
        self.assertEqual(self.rfq.status, 'REVIEWING')
        self.assertEqual(self.rfq.admin_notes, 'Allocated to Tamil Nadu supplier for sample testing.')

    def test_rfq_csv_export(self):
        self.client.login(username='staff_test', password='Password123!')
        response = self.client.get(reverse('dashboard:rfq_export'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('STELLAR-2026-TEST', response.content.decode('utf-8'))
        self.assertIn('Buyer Corp', response.content.decode('utf-8'))

    def test_staff_product_specs_update(self):
        self.client.login(username='staff_test', password='Password123!')
        url = reverse('dashboard:product_edit', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Submit updated specs using the visual row format
        post_data = {
            'name': 'Test Banana Fiber',
            'category': self.cat.id,
            'tagline': 'Textile grade',
            'description': 'High tensile test fiber',
            'raw_material': 'Pseudostem',
            'extraction_method': 'Mechanical',
            'processing': 'Cleaned',
            'harvest_origin': 'Tamil Nadu',
            'moq': '500 kg',
            'packaging_details': 'LDPE inner liner',
            'hs_code': '5305.00',
            'display_order': 1,
            'is_active': 'on',
            'applications_raw': 'Yarn Spinning\nComposite Reinforcement',
            'spec_key[]': ['Moisture Content', 'Fiber Length', 'Tensile Strength'],
            'spec_val[]': ['10% - 12%', '4-5 ft', '30-40 cN/tex'],
            'spec_note[]': ['Oven dried', 'Manual measurement', 'Test-measured'],
            'spec_type[]': ['provisional', 'provisional', 'verified']
        }
        resp_post = self.client.post(url, post_data, follow=True)
        self.assertEqual(resp_post.status_code, 200)

        self.product.refresh_from_db()
        self.assertIn('Moisture Content', self.product.provisional_specs)
        self.assertIn('Fiber Length', self.product.provisional_specs)
        self.assertIn('Tensile Strength', self.product.verified_specs)
        self.assertEqual(self.product.applications, ['Yarn Spinning', 'Composite Reinforcement'])

        # Verify that changes show up on the public product detail page
        resp_detail = self.client.get(reverse('products:detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(resp_detail.status_code, 200)
        self.assertContains(resp_detail, 'High tensile test fiber')
        self.assertContains(resp_detail, 'Yarn Spinning')
        self.assertContains(resp_detail, 'Composite Reinforcement')
        self.assertContains(resp_detail, 'Moisture Content')
        self.assertContains(resp_detail, '10% - 12%')
        self.assertContains(resp_detail, 'Tensile Strength')
        self.assertContains(resp_detail, 'Tamil Nadu')

    def test_staff_faq_crud(self):
        self.client.login(username='staff_test', password='Password123!')
        
        # Create FAQ
        create_url = reverse('dashboard:faq_create')
        resp_create = self.client.post(create_url, {
            'category': 'LOGISTICS',
            'question': 'Can you coordinate port delivery?',
            'answer': 'Yes, shipping terms and logistics are confirmed for each order.',
            'display_order': 5,
            'is_active': 'on'
        }, follow=True)
        self.assertEqual(resp_create.status_code, 200)
        new_faq = FAQ.objects.filter(question__icontains='port delivery').first()
        self.assertIsNotNone(new_faq)

        # Update FAQ
        update_url = reverse('dashboard:faq_update', kwargs={'pk': new_faq.pk})
        resp_update = self.client.post(update_url, {
            'category': 'LOGISTICS',
            'question': 'Can you coordinate port delivery and customs?',
            'answer': 'Updated answer.',
            'display_order': 2,
            'is_active': 'on'
        }, follow=True)
        self.assertEqual(resp_update.status_code, 200)
        new_faq.refresh_from_db()
        self.assertEqual(new_faq.question, 'Can you coordinate port delivery and customs?')

        # Delete FAQ
        delete_url = reverse('dashboard:faq_delete', kwargs={'pk': new_faq.pk})
        resp_delete = self.client.post(delete_url, follow=True)
        self.assertEqual(resp_delete.status_code, 200)
        self.assertFalse(FAQ.objects.filter(pk=new_faq.pk).exists())
