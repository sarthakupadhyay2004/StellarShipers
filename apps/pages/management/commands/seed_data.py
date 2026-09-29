from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.products.models import Category, Product
from apps.pages.models import FAQ
from apps.rfq.models import RFQ

class Command(BaseCommand):
    help = 'Seeds production-grade initial fixtures for STELLAR SHIPERS per Handoff Doc'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database with updated handoff specifications...')

        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'stellarshipper45@gmail.com', 'stellar2026!')
            self.stdout.write(self.style.SUCCESS('Superuser "admin" created.'))

        # 2. Categories
        cat_fibers, _ = Category.objects.get_or_create(
            slug='natural-plant-fibers',
            defaults={
                'name': 'Natural Plant Fibers',
                'description': 'Raw and semi-processed natural fibers for textile and non-woven manufacturing.',
                'display_order': 1
            }
        )

        # 3. Featured Product: Textile-Grade Raw Banana Fiber (Single Catalog Product)
        Product.objects.all().delete()
        Product.objects.create(
            category=cat_fibers,
            slug='banana-fiber',
            name='Textile-grade raw banana fiber',
            tagline='Unspun, extracted from Musa plant pseudostems for natural-fiber/textile applications',
            description=(
                'Natural, mechanically extracted and dried banana fiber sourced from G9 banana pseudostems, '
                'supplied in cleaned/combed fiber bundles for textile and natural-fiber applications.'
            ),
            raw_material='Musa plant pseudostems',
            extraction_method='Mechanical decortication',
            processing='Drying only; cleaned/combed fiber bundles; no chemical treatment.',
            supplier_notes='Supplier capacity: 15 MT/month. Packaging: inner LDPE liner and outer woven HDPE sacks.',
            harvest_origin='Jalgaon, Maharashtra, India',
            moq='500 kg',
            packaging_details='Inner LDPE liner and outer woven HDPE sacks for long-distance export transport.',
            hs_code='5305.00',
            applications=[
                'Natural-fiber textile development',
                'Blended yarn / textile development where technically suitable',
                'Woven or nonwoven material development',
                'Home-textile and furnishing applications',
                'Craft, specialty and other natural-fiber applications'
            ],
            verified_specs={},
            provisional_specs={
                'Banana Variety': {'value': 'G9', 'note': 'Supplier-stated'},
                'Raw Material': {'value': 'Musa plant pseudostems', 'note': 'Confirmed'},
                'Extraction': {'value': 'Mechanical', 'note': 'Confirmed'},
                'Post-extraction processing': {'value': 'Drying only', 'note': 'Supplier-stated'},
                'Chemical treatment': {'value': 'No chemical treatment / 100% natural', 'note': 'Supplier-stated'},
                'Typical fiber length': {'value': 'upto 5 ft', 'note': 'Supplier-stated'},
                'Colour': {'value': 'Golden', 'note': 'Supplier-stated / visually apparent'},
                'Tensile Strength': {'value': 'test-measured per buyer specification', 'note': 'Testing on-demand'},
                'Moisture': {'value': 'Requires accredited laboratory testing before export', 'note': 'Testing required'}
            },
            is_featured=True,
            is_active=True,
            display_order=1
        )
        self.stdout.write(self.style.SUCCESS('Product "Textile-grade raw banana fiber" updated.'))

        # 4. FAQs
        FAQ.objects.all().delete()
        faq_items = [
            ('SOURCING', 'Where is the raw banana fiber produced?', 'The initial raw banana fiber is produced in Jalgaon, Maharashtra, India—one of the largest banana cultivation belts in Asia. STELLAR SHIPERS oversees quality verification and export logistics from origin to international destinations.'),
            ('SAMPLES', 'Can we request a physical fiber sample for spinning trials?', 'Yes. We encourage textile and yarn manufacturers to request an evaluation sample kit to test runnability, fineness, and fiber length on their specific machinery. Simply select "Request Product Sample" on our RFQ form.'),
            ('SAMPLES', 'Do you charge for samples?', 'Samples are complimentary; customers are only responsible for the actual shipping and delivery expenses. You may either provide your own courier account details for freight collect or have us calculate and invoice the shipping fee directly.'),
            ('LOGISTICS', 'What is the Minimum Order Quantity (MOQ)?', 'The MOQ is 500 kg, which can be scaled up to full container loads (FCL 20ft/40ft) with a monthly supplier capacity of 15 MT/month.'),
            ('LOGISTICS', 'What are your primary export destinations?', 'Our primary focus includes European markets such as Germany, France, Portugal, Sweden, and Switzerland, alongside international natural-fiber wholesalers and distributors across the globe.'),
            ('COMMERCIAL', 'How are prices quoted?', 'We do not publish fixed public retail prices. Prices are quoted based on required volume, packaging specifications, destination port, and applicable Incoterms (FOB, CIF, CFR).')
        ]
        for cat, q, a in faq_items:
            FAQ.objects.create(category=cat, question=q, answer=a, is_active=True)

        self.stdout.write(self.style.SUCCESS('Database re-seeded successfully with updated specifications.'))
