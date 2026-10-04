from django.db import models

class CompanyProfile(models.Model):
    """
    Singleton model representing the core corporate profile, contact coordinates,
    tax & DGFT registrations (GSTIN, IEC), and trade scope disclaimers.
    """
    company_name = models.CharField(max_length=200, default='STELLAR SHIPERS')
    primary_email = models.EmailField(default='contact@stellarshipers.com', help_text='Primary corporate email address')
    primary_phone = models.CharField(max_length=100, default='Available upon inquiry / B2B RFQ', help_text='Corporate telephone or desk contact')
    address = models.CharField(max_length=255, default='India', blank=True, help_text='Registered office jurisdiction')
    
    # Trade Registrations (Tax & Export Licensing)
    gstin = models.CharField(max_length=25, blank=True, null=True, help_text='15-character Indian Goods & Services Tax Identification Number (e.g. 07AAAAA0000A1Z5)')
    iec = models.CharField(max_length=25, blank=True, null=True, help_text='10-digit DGFT Importer-Exporter Code issued by Govt of India')
    show_gstin = models.BooleanField(default=True, help_text='Display GSTIN publicly on website footer and trade documentation areas')
    show_iec = models.BooleanField(default=True, help_text='Display IEC publicly on website footer and trade documentation areas')
    
    # Anti-Courier / Scam Disambiguation
    operational_scope = models.CharField(
        max_length=350, 
        default='B2B Maritime Cargo & Bulk Agro-Industrial Export Coordination (Exclusively wholesale freight; not a consumer parcel courier or retail package tracking entity).',
        help_text='Public scope statement preventing automated confusion with retail courier/parcel delivery tracking'
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company Profile & Registration'
        verbose_name_plural = 'Company Profile & Registrations'

    def __str__(self):
        return f"{self.company_name} Profile"

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj


class SocialLink(models.Model):
    """
    Dynamic social media channel links managed via the Operations Dashboard.
    """
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
        ('twitter', 'X (Twitter)'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('whatsapp', 'WhatsApp'),
        ('other', 'Other Platform'),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='linkedin')
    display_name = models.CharField(max_length=100, help_text='Display label (e.g. "LinkedIn", "Instagram", "WhatsApp Desk")')
    url = models.URLField(max_length=500, help_text='Full target URL (e.g. https://www.linkedin.com/company/stellarshipers)')
    is_active = models.BooleanField(default=True, help_text='Controls whether this channel is displayed publicly')
    display_order = models.PositiveIntegerField(default=0, help_text='Lower values appear first')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Social Media Channel'
        verbose_name_plural = 'Social Media Channels'

    def __str__(self):
        return f"{self.get_platform_display()} - {self.display_name} ({self.url})"
