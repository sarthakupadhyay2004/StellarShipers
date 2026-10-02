from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True, help_text="Brief commercial summary")
    description = models.TextField(help_text="Detailed industrial overview of product")

    # Production & Processing Specs
    raw_material = models.CharField(max_length=255, help_text="Botanical / origin feedstock (e.g. Musa acuminata pseudostem)")
    extraction_method = models.TextField(help_text="Mechanical decortication, chemical, or biological retting")
    processing = models.TextField(help_text="Post-extraction drying, combing, carding, degumming, sorting")
    supplier_notes = models.TextField(blank=True, help_text="Supplier-reported observations, lot variability, seasonal supply factors")

    # Technical Specification Partitioning (Crucial Requirement: No unverified data presented as certified)
    verified_specs = models.JSONField(
        default=dict,
        blank=True,
        help_text="Structured dict of certified laboratory-tested metrics. E.g.: {'Tensile Strength': {'value': '580-720 MPa', 'test_method': 'ASTM D3822', 'tolerance': '±5%'}}"
    )
    provisional_specs = models.JSONField(
        default=dict,
        blank=True,
        help_text="Structured dict of supplier-reported / provisional estimates. E.g.: {'Estimated Microfibril Angle': {'value': '11°-13°', 'status': 'Supplier Estimated - Pending Lab Confirmation'}}"
    )

    # Sourcing & Trade Terms
    harvest_origin = models.CharField(max_length=150, blank=True, default="Direct Mill Origins / Certified Estates")
    moq = models.CharField(max_length=100, default="1 FCL / 10 Metric Tons", help_text="Minimum Order Quantity")
    packaging_details = models.TextField(blank=True, help_text="Hydraulically compressed bales, palletized, PP wrapping, custom moisture barrier")
    hs_code = models.CharField(max_length=50, blank=True, help_text="Harmonized System Tariff Code")
    applications = models.JSONField(default=list, blank=True, help_text="List of industrial use cases (e.g. Automotive, Paper, Textile)")

    # Status & Visibility
    is_featured = models.BooleanField(default=False, help_text="Feature prominently on homepage")
    is_active = models.BooleanField(default=True, help_text="Display publicly on catalog")
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    @property
    def primary_image(self):
        primary = self.images.filter(is_primary=True).first()
        if primary:
            return primary
        return self.images.first()

    @property
    def formatted_specs(self):
        """
        Returns a normalized list of specification dicts:
        [{'name': key, 'value': value, 'note': note, 'is_verified': bool}, ...]
        Verified parameters are listed first, followed by provisional parameters.
        """
        specs = []
        seen = set()
        if isinstance(self.verified_specs, dict):
            for k, v in self.verified_specs.items():
                val = v.get('value', '') if isinstance(v, dict) else str(v)
                note = v.get('note', '') if isinstance(v, dict) else ''
                specs.append({'name': k, 'value': val, 'note': note, 'is_verified': True})
                seen.add(k.lower())
        if isinstance(self.provisional_specs, dict):
            for k, v in self.provisional_specs.items():
                val = v.get('value', '') if isinstance(v, dict) else str(v)
                note = v.get('note', '') if isinstance(v, dict) else ''
                specs.append({'name': k, 'value': val, 'note': note, 'is_verified': False})
                seen.add(k.lower())

        # Include core botanical and extraction specs if not explicitly overridden in specs
        if self.raw_material and 'raw material' not in seen and 'raw material source' not in seen:
            specs.insert(0 if not specs else 1, {
                'name': 'Raw Material Source',
                'value': self.raw_material,
                'note': 'Confirmed',
                'is_verified': False
            })
            seen.add('raw material source')

        if self.extraction_method and 'extraction' not in seen and 'extraction method' not in seen:
            specs.append({
                'name': 'Extraction Method',
                'value': self.extraction_method,
                'note': 'Confirmed',
                'is_verified': False
            })
            seen.add('extraction method')

        if self.processing and 'processing' not in seen and 'post-extraction processing' not in seen:
            specs.append({
                'name': 'Post-Extraction Processing',
                'value': self.processing,
                'note': 'Supplier-stated',
                'is_verified': False
            })

        return specs

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/images/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"Image for {self.product.name} ({'Primary' if self.is_primary else 'Gallery'})"


class ProductDocument(models.Model):
    DOC_TYPES = [
        ('TDS', 'Technical Data Sheet (TDS)'),
        ('COA', 'Certificate of Analysis (COA)'),
        ('SPEC', 'Technical Specifications Summary'),
        ('COMPLIANCE', 'Phytosanitary / Export Compliance Document'),
    ]

    product = models.ForeignKey(Product, related_name='documents', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES, default='TDS')
    document_file = models.FileField(upload_to='products/documents/')
    file_size = models.CharField(max_length=50, blank=True, help_text="e.g. '340 KB PDF'")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_doc_type_display()} - {self.title} ({self.product.name})"
