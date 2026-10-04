from datetime import datetime

def site_settings(request):
    """
    Context processor injecting corporate identity, trade registrations,
    and dynamic social media channels across all templates.
    """
    from .models import CompanyProfile, SocialLink

    profile = None
    social_links = []
    try:
        profile = CompanyProfile.get_solo()
        social_links = list(SocialLink.objects.filter(is_active=True).order_by('display_order', 'id'))
    except Exception:
        # Graceful fallback during database migrations or table initialization
        pass

    primary_email = profile.primary_email if profile and profile.primary_email else 'contact@stellarshipers.com'
    primary_phone = profile.primary_phone if profile and profile.primary_phone else 'Available upon inquiry / B2B RFQ'
    
    gstin = profile.gstin.strip() if profile and profile.gstin and profile.show_gstin else None
    iec = profile.iec.strip() if profile and profile.iec and profile.show_iec else None
    operational_scope = profile.operational_scope if profile and profile.operational_scope else 'B2B Maritime Cargo & Bulk Agro-Industrial Export Coordination (Exclusively wholesale freight; not a consumer parcel courier or retail package tracking entity).'

    return {
        'SITE_NAME': profile.company_name if profile and profile.company_name else 'STELLAR SHIPERS',
        'SITE_LEGAL_NAME': 'STELLAR SHIPERS',
        'SITE_TAGLINE': 'WHERE TRUST MEETS VALUE.',
        'SITE_SUPPORTING_LINE': 'Indian sourcing. International standards. Responsible export coordination.',
        'SITE_SUBTITLE': 'India-based international sourcing and export company connecting carefully selected Indian producers with global B2B buyers.',
        'PRIMARY_EMAIL': primary_email,
        'PRIMARY_PHONE': primary_phone,
        'GSTIN': gstin,
        'IEC': iec,
        'SHOW_GSTIN': profile.show_gstin if profile else True,
        'SHOW_IEC': profile.show_iec if profile else True,
        'OPERATIONAL_SCOPE': operational_scope,
        'COMPANY_PROFILE': profile,
        'SOCIAL_LINKS': social_links,
        'CURRENT_YEAR': datetime.now().year,
    }
