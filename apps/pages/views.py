from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse
from apps.products.models import Product
from apps.pages.models import FAQ, PageContent
from apps.rfq.forms import RFQForm

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 1. Featured product (Banana fiber priority)
        banana_fiber = Product.objects.filter(is_active=True, name__icontains='banana').first()
        if not banana_fiber:
            banana_fiber = Product.objects.filter(is_active=True, is_featured=True).first()
        context['featured_product'] = banana_fiber

        # Other active products for preview
        context['catalog_products'] = Product.objects.filter(is_active=True).exclude(id=getattr(banana_fiber, 'id', None))[:3]

        # RFQ form for embedded CTA section
        context['rfq_form'] = RFQForm()

        # Meta tags
        context['meta_title'] = 'STELLAR SHIPERS | B2B Sourcing, Technical Verification & Global Export'
        context['meta_desc'] = 'WHERE TRUST MEETS VALUE. Certified agro-industrial raw materials, natural fibers, and direct mill sourcing with verified laboratory specifications.'
        return context


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = 'About Us | STELLAR SHIPERS - Sourcing & Export Governance'
        context['meta_desc'] = 'Learn about Stellar Shipers: our origin sourcing network, strict technical integrity standards, and international B2B export capabilities.'
        return context


class QualityProcessView(TemplateView):
    template_name = 'pages/quality_process.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = 'Quality & Verification Process | STELLAR SHIPERS'
        context['meta_desc'] = 'Source → Verify → Coordinate → Export. Our rigorous 4-step quality protocol ensuring certified technical data and zero untested claims.'
        return context


class ServicesView(TemplateView):
    template_name = 'pages/services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = 'Sourcing Services | STELLAR SHIPERS'
        context['meta_desc'] = 'From requirement to reliable supply. We help international B2B buyers source selected natural fibers and sustainable materials from India according to clear specifications.'
        return context


class ContactView(TemplateView):
    template_name = 'pages/contact_rfq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RFQForm()
        context['meta_title'] = 'Contact Export Desk & RFQ | STELLAR SHIPERS'
        context['meta_desc'] = 'Directly contact our international trade team or submit a technical Request for Quotation (RFQ). Fast response within 24-48 business hours.'
        return context


class FAQView(TemplateView):
    template_name = 'pages/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        faqs = FAQ.objects.filter(is_active=True).order_by('category', 'display_order')
        
        # Group by category
        grouped_faqs = {}
        for faq in faqs:
            cat_name = faq.get_category_display()
            if cat_name not in grouped_faqs:
                grouped_faqs[cat_name] = []
            grouped_faqs[cat_name].append(faq)

        context['grouped_faqs'] = grouped_faqs
        context['faqs'] = faqs
        context['meta_title'] = 'Frequently Asked Questions (FAQ) | STELLAR SHIPERS'
        context['meta_desc'] = 'Answers to common questions regarding our technical verification protocols, sample evaluation kits, MOQ, Incoterms, and payment contracts.'
        return context


class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = 'Privacy Policy | STELLAR SHIPERS'
        context['meta_desc'] = 'Commercial data protection and privacy policy for B2B buyers, sourcing inquiries, and quotation records.'
        return context


class TermsOfUseView(TemplateView):
    template_name = 'pages/terms.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_title'] = 'Terms of Use & Trade Governance | STELLAR SHIPERS'
        context['meta_desc'] = 'Commercial B2B terms covering quotation validity, sample evaluation agreements, specification tolerances, and export compliance.'
        return context


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /rfq/success/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
