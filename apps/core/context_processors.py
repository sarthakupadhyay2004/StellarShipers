from datetime import datetime

def site_settings(request):
    return {
        'SITE_NAME': 'STELLAR SHIPERS',
        'SITE_LEGAL_NAME': 'STELLAR SHIPERS',
        'SITE_TAGLINE': 'WHERE TRUST MEETS VALUE.',
        'SITE_SUPPORTING_LINE': 'Indian sourcing. International standards. Responsible export coordination.',
        'SITE_SUBTITLE': 'India-based international sourcing and export company connecting carefully selected Indian producers with global B2B buyers.',
        'PRIMARY_EMAIL': 'stellarshipper45@gmail.com',
        'PRIMARY_PHONE': 'Available upon inquiry / B2B RFQ',
        'CURRENT_YEAR': datetime.now().year,
    }

