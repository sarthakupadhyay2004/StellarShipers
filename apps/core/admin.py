from django.contrib import admin
from .models import CompanyProfile, SocialLink

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'primary_email', 'gstin', 'iec', 'show_gstin', 'show_iec', 'updated_at')
    fieldsets = (
        ('Corporate Information', {
            'fields': ('company_name', 'primary_email', 'primary_phone', 'address')
        }),
        ('Tax & DGFT Trade Registrations', {
            'fields': ('gstin', 'show_gstin', 'iec', 'show_iec')
        }),
        ('Anti-Fraud & Operating Scope Disambiguation', {
            'fields': ('operational_scope',)
        }),
    )

    def has_add_permission(self, request):
        # Prevent creating multiple singleton records
        return not CompanyProfile.objects.exists()


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'platform', 'url', 'is_active', 'display_order', 'updated_at')
    list_editable = ('is_active', 'display_order')
    list_filter = ('platform', 'is_active')
    search_fields = ('display_name', 'url')
