from django.urls import path
from .views import (
    DashboardLoginView, DashboardLogoutView,
    DashboardHomeView,
    DashboardRFQListView, DashboardRFQDetailView, DashboardRFQExportCSVView,
    DashboardProductListView, DashboardProductEditView,
    DashboardFAQListView, DashboardFAQCreateView, DashboardFAQUpdateView, DashboardFAQDeleteView
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardHomeView.as_view(), name='home'),
    path('login/', DashboardLoginView.as_view(), name='login'),
    path('logout/', DashboardLogoutView.as_view(), name='logout'),
    
    # RFQs Pipeline
    path('rfqs/', DashboardRFQListView.as_view(), name='rfq_list'),
    path('rfqs/export/', DashboardRFQExportCSVView.as_view(), name='rfq_export'),
    path('rfqs/<int:pk>/', DashboardRFQDetailView.as_view(), name='rfq_detail'),

    # Products & Technical Specs
    path('products/', DashboardProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/edit/', DashboardProductEditView.as_view(), name='product_edit'),

    # FAQ Knowledge Base
    path('faqs/', DashboardFAQListView.as_view(), name='faq_list'),
    path('faqs/add/', DashboardFAQCreateView.as_view(), name='faq_create'),
    path('faqs/<int:pk>/edit/', DashboardFAQUpdateView.as_view(), name='faq_update'),
    path('faqs/<int:pk>/delete/', DashboardFAQDeleteView.as_view(), name='faq_delete'),
]
