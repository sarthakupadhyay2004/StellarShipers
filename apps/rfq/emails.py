import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)

def send_rfq_notifications(rfq):
    """
    Sends notification email to internal admin desk and
    automated receipt confirmation to prospective buyer.
    """
    product_name = rfq.product.name if rfq.product else (rfq.product_interest or "Custom Sourcing Inquiry")

    # 1. Internal Admin Alert
    admin_subject = f"[NEW RFQ] {rfq.reference_id} - {rfq.company} ({product_name}) - {rfq.country}"
    admin_context = {
        'rfq': rfq,
        'product_name': product_name,
        'site_name': getattr(settings, 'SITE_NAME', 'STELLAR SHIPERS'),
    }

    admin_body = f"""
NEW B2B RFQ RECEIVED
--------------------------------------------------
Reference ID: {rfq.reference_id}
Status: {rfq.get_status_display()}
Date: {rfq.created_at.strftime('%Y-%m-%d %H:%M UTC')}

BUYER DETAILS:
Company: {rfq.company}
Contact: {rfq.name}
Country: {rfq.country}
Corporate Email: {rfq.email}
Phone/WhatsApp: {rfq.phone or 'Not provided'}

PRODUCT & SOURCING PARAMETERS:
Target Product: {product_name}
Estimated Volume: {rfq.quantity}
Intended Application: {rfq.application}
Sample Kit Requested: {'YES (Physical sample required)' if rfq.sample_request else 'No'}

LOGISTICS & SPECS:
Packaging: {rfq.packaging}
Destination Country/Port: {rfq.delivery_country}
Incoterms: {rfq.get_incoterms_display()}
Technical Requirements:
{rfq.technical_requirements or 'None specified'}

Additional Notes:
{rfq.message or 'None'}

File Attached: {'YES' if rfq.technical_file else 'No'}{f'''
File Download URL: {rfq.technical_file.url}''' if rfq.technical_file else ''}
--------------------------------------------------
Review in Django Admin: /admin/rfq/rfq/{rfq.pk}/change/
"""

    try:
        send_mail(
            subject=admin_subject,
            message=admin_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_NOTIFICATION_EMAIL],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send admin RFQ notification for {rfq.reference_id}: {e}")

    # 2. Buyer Acknowledgment Email
    buyer_subject = f"Receipt Confirmation: Your Sourcing RFQ [{rfq.reference_id}] - STELLAR SHIPERS"
    buyer_body = f"""
Dear {rfq.name},

Thank you for your commercial sourcing inquiry with STELLAR SHIPERS.

We have registered your Request for Quotation under reference: {rfq.reference_id}

INQUIRY SUMMARY:
- Organization: {rfq.company}
- Product / Commodity: {product_name}
- Volume: {rfq.quantity}
- Delivery Destination: {rfq.delivery_country}
- Incoterms: {rfq.get_incoterms_display()}
- Sample Request: {'Physical Sample Kit Requested' if rfq.sample_request else 'Standard Quotation'}

OUR SOURCING DESK COMMITMENT:
In alignment with our founding principle—WHERE TRUST MEETS VALUE—all commercial quotes are issued with verified technical tolerances, direct-mill origin validation, and full chain-of-custody transparency.

Our technical sourcing desk is currently reviewing your technical requirements. An export specialist will contact you within 24–48 business hours with preliminary technical specifications and quotation parameters.

If you have urgent revisions or supplementary technical dossiers to submit, please reply directly to this message referencing [{rfq.reference_id}].

Sincerely,

Global Export Operations Desk
STELLAR SHIPERS
"WHERE TRUST MEETS VALUE."
Web: www.stellarshipers.com
Email: {settings.DEFAULT_FROM_EMAIL}
"""

    try:
        send_mail(
            subject=buyer_subject,
            message=buyer_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[rfq.email],
            fail_silently=True,
        )
    except Exception as e:
        logger.error(f"Failed to send buyer acknowledgment for {rfq.reference_id}: {e}")
