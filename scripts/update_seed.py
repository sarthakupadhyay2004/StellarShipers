seed_code = '''from django.core.management.base import BaseCommand
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
            User.objects.create_superuser('admin', 'contact@stellarshipers.com', 'stellar2026!')
            self.stdout.write(self.style.SUCCESS('Superuser \"admin\" created.'))

        # 2. Categories
        cat_fibers, _ = Category.objects.get_or_create(
            slug='natural-plant-fibers',
            defaults={
                'name': 'Natural Plant Fibers',
                'description': 'Raw and semi-processed natural fibers for textile and non-woven manufacturing.',
                'display_order': 1
            }
        )

        # 3. Featured Product: Textile-Grade Raw Banana Fiber (Page 5)
        Product.objects.filter(slug='banana-fiber').delete()
        Product.objects.create(
            category=cat_fibers,
            slug='banana-fiber',
            name='Textile-grade raw banana fiber',
            tagline='Unspun, extracted from Musa plant pseudostems for natural-fiber/textile applications',
            description=(
                'Natural, mechanically extracted and dried banana fiber sourced from G9 banana pseudostems, '
                'supplied in cleaned/combed fiber bundles for textile and natural-fiber applications.'
            ),
            raw_material='Musa plant pseudostems (G9 Grand Naine)',
            extraction_method='Mechanical decortication',
            processing='Drying only; cleaned/combed fiber bundles; no chemical treatment.',
            supplier_notes='Supplier location: Jalgaon, Maharashtra, India. Stored fiber stated to be available for dispatch. Expandable capacity 5-10 MT/month.',
            harvest_origin='Jalgaon, Maharashtra, India',
            moq='500 kg (Supplier-stated)',
            packaging_details='Polythene / poly-woven bags recommended for long-distance export transport.',
            hs_code='5305.00',
            applications=[
                'Natural-fiber textile development',
                'Blended yarn / textile development where technically suitable',
                'Woven or nonwoven material development',
                'Home-textile and furnishing applications',
                'Craft, specialty and other natural-fiber applications'
            ],
            verified_specs={},  # Do not publish generic internet lab values per Page 3 & 5
            provisional_specs={
                'Banana Variety': {'value': 'G9 (Grand Naine)', 'note': 'Supplier-stated'},
                'Raw Material': {'value': 'Musa plant pseudostems', 'note': 'Confirmed'},
                'Extraction': {'value': 'Mechanical', 'note': 'Confirmed'},
                'Post-extraction processing': {'value': 'Drying only', 'note': 'Supplier-stated'},
                'Chemical treatment': {'value': 'No chemical treatment / 100% natural', 'note': 'Supplier-stated'},
                'Typical fiber length': {'value': 'Approx. 4–5 ft', 'note': 'Supplier-stated'},
                'Colour': {'value': 'Golden', 'note': 'Supplier-stated / visually apparent'},
                'Tensile & Fineness': {'value': 'Conducted per buyer specification', 'note': 'Testing on-demand'},
                'Moisture': {'value': 'Requires accredited laboratory testing before export', 'note': 'Testing required'}
            },
            is_featured=True,
            is_active=True,
            display_order=1
        )
        self.stdout.write(self.style.SUCCESS('Product \"Textile-grade raw banana fiber\" updated per Page 5.'))

        # 4. FAQs
        FAQ.objects.all().delete()
        faq_items = [
            ('SOURCING', 'Where is the raw banana fiber produced?', 'The initial raw banana fiber is produced in Jalgaon, Maharashtra, India—one of the largest banana cultivation belts in Asia. STELLAR SHIPERS oversees quality verification and export logistics from origin to international destinations.'),
            ('SOURCING', 'What is your operational model?', 'We operate on a Buy & Resell / sourcing + export coordination model. Supplier production is external. We take full responsibility for requirement review, quality verification before export, reasonable customization, and disciplined export documentation.'),
            ('SPECS', 'Why are generic tensile strength numbers not published on the website?', 'In strict compliance with our Specification Integrity standard (Page 5), we refuse to publish untested generic internet numbers as certified data. Tensile strength, fineness, and moisture parameters are formally verified by third-party testing laboratories according to buyer-specific testing protocols.'),
            ('SAMPLES', 'Can we request a physical fiber sample for spinning trials?', 'Yes. We encourage European textile and yarn manufacturers to request an evaluation sample kit to test runnability, fineness, and fiber length on their specific machinery. Simply select \"Request Product Sample\" on our RFQ form.'),
            ('LOGISTICS', 'What is the Minimum Order Quantity (MOQ)?', 'The supplier-stated MOQ is 500 kg, which can be scaled up to full container loads (FCL 20ft/40ft) with an expandable monthly capacity of 5–10 MT/month.'),
            ('LOGISTICS', 'What are your primary export destinations?', 'Our primary focus is Europe, specifically Germany and France, alongside international natural-fiber wholesalers and distributors across the globe.'),
            ('COMMERCIAL', 'How are prices quoted?', 'We do not publish fixed public retail prices. Prices are quoted based on required volume, packaging specifications, destination port, and applicable Incoterms (FOB, CIF, CFR).')
        ]
        for cat, q, a in faq_items:
            FAQ.objects.create(category=cat, question=q, answer=a, is_active=True)

        self.stdout.write(self.style.SUCCESS('Database re-seeded successfully according to Handoff Doc.'))
'''

with open('apps/pages/management/commands/seed_data.py', 'w', encoding='utf-8') as f:
    f.write(seed_code)
print('seed_data.py updated')
