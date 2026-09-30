from django.urls import path
from .views import (
    HomeView, AboutView, QualityProcessView, ServicesView,
    ContactView, FAQView, PrivacyPolicyView, TermsOfUseView,
    robots_txt
)

app_name = 'pages'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('quality-process/', QualityProcessView.as_view(), name='quality_process'),
    path('services/', ServicesView.as_view(), name='services'),
    path('contact-rfq/', ContactView.as_view(), name='contact'),
    path('contact/', ContactView.as_view()),
    path('faq/', FAQView.as_view(), name='faq'),
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy'),
    path('terms-of-use/', TermsOfUseView.as_view(), name='terms'),
    path('robots.txt', robots_txt, name='robots'),
]
