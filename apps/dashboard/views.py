import csv
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from apps.rfq.models import RFQ
from apps.products.models import Product, Category
from apps.pages.models import FAQ
from apps.core.models import CompanyProfile, SocialLink
from .forms import (
    DashboardLoginForm, DashboardRFQStatusForm, DashboardFAQForm, DashboardProductForm,
    DashboardCompanyProfileForm, DashboardSocialLinkForm
)

class AdminRequiredMixin(UserPassesTestMixin):
    login_url = 'dashboard:login'

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_staff or user.is_superuser)

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f"{reverse('dashboard:login')}?next={self.request.path}")
        messages.error(self.request, "Access restricted. Staff or administrator credentials required.")
        return render(self.request, 'dashboard/403.html', status=403)


class DashboardLoginView(LoginView):
    template_name = 'dashboard/login.html'
    form_class = DashboardLoginForm
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url and next_url.startswith('/dashboard/'):
            return next_url
        return reverse_lazy('dashboard:home')


class DashboardLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been logged out of the Operations Dashboard.")
        return redirect('dashboard:login')

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, "You have been logged out of the Operations Dashboard.")
        return redirect('dashboard:login')


class DashboardHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_rfqs'] = RFQ.objects.count()
        context['new_rfqs'] = RFQ.objects.filter(status='NEW').count()
        context['reviewing_rfqs'] = RFQ.objects.filter(status='REVIEWING').count()
        context['sample_rfqs'] = RFQ.objects.filter(sample_request=True).count()
        context['active_products'] = Product.objects.filter(is_active=True).count()
        context['total_faqs'] = FAQ.objects.filter(is_active=True).count()
        context['recent_rfqs'] = RFQ.objects.select_related('product')[:8]
        return context


class DashboardRFQListView(AdminRequiredMixin, ListView):
    model = RFQ
    template_name = 'dashboard/rfq_list.html'
    context_object_name = 'rfqs'
    paginate_by = 25

    def get_queryset(self):
        qs = RFQ.objects.select_related('product')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        sample = self.request.GET.get('sample')
        if sample == '1':
            qs = qs.filter(sample_request=True)
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(
                Q(company__icontains=q) |
                Q(name__icontains=q) |
                Q(email__icontains=q) |
                Q(country__icontains=q) |
                Q(delivery_country__icontains=q) |
                Q(reference_id__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', '')
        context['current_sample'] = self.request.GET.get('sample', '')
        context['search_query'] = self.request.GET.get('q', '')
        context['status_choices'] = RFQ.STATUS_CHOICES
        return context


class DashboardRFQDetailView(AdminRequiredMixin, UpdateView):
    model = RFQ
    form_class = DashboardRFQStatusForm
    template_name = 'dashboard/rfq_detail.html'
    context_object_name = 'rfq'

    def get_success_url(self):
        messages.success(self.request, f"Inquiry {self.object.reference_id} status updated successfully.")
        return reverse('dashboard:rfq_detail', kwargs={'pk': self.object.pk})


class DashboardRFQExportCSVView(AdminRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="stellar_shipers_rfqs.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Reference ID', 'Date', 'Status', 'Company', 'Contact Name',
            'Email', 'Phone', 'Buyer Country', 'Destination Port', 'Product',
            'Quantity', 'Application', 'Incoterms', 'Sample Request', 'Packaging',
            'Technical Specs', 'Buyer Message', 'Staff Notes'
        ])
        for r in RFQ.objects.select_related('product').all():
            writer.writerow([
                r.reference_id,
                r.created_at.strftime('%Y-%m-%d %H:%M'),
                r.get_status_display(),
                r.company,
                r.name,
                r.email,
                r.phone,
                r.country,
                r.delivery_country,
                r.product.name if r.product else r.product_interest,
                r.quantity,
                r.application,
                r.get_incoterms_display(),
                'Yes' if r.sample_request else 'No',
                r.packaging,
                r.technical_requirements,
                r.message,
                r.admin_notes
            ])
        return response


class DashboardProductListView(AdminRequiredMixin, ListView):
    model = Product
    template_name = 'dashboard/product_list.html'
    context_object_name = 'products'


class DashboardProductEditView(AdminRequiredMixin, UpdateView):
    model = Product
    form_class = DashboardProductForm
    template_name = 'dashboard/product_edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        # Flatten specifications for the visual row editor
        spec_rows = []
        if isinstance(product.provisional_specs, dict):
            for k, v in product.provisional_specs.items():
                spec_rows.append({
                    'key': k,
                    'value': v.get('value', '') if isinstance(v, dict) else str(v),
                    'note': v.get('note', '') if isinstance(v, dict) else '',
                    'spec_type': 'provisional'
                })
        if isinstance(product.verified_specs, dict):
            for k, v in product.verified_specs.items():
                spec_rows.append({
                    'key': k,
                    'value': v.get('value', '') if isinstance(v, dict) else str(v),
                    'note': v.get('note', '') if isinstance(v, dict) else '',
                    'spec_type': 'verified'
                })
        context['spec_rows'] = spec_rows
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        # Parse visual specification rows from POST data
        spec_keys = self.request.POST.getlist('spec_key[]')
        spec_values = self.request.POST.getlist('spec_val[]')
        spec_notes = self.request.POST.getlist('spec_note[]')
        spec_types = self.request.POST.getlist('spec_type[]')

        new_provisional = {}
        new_verified = {}

        for i in range(len(spec_keys)):
            k = spec_keys[i].strip()
            if not k:
                continue
            val = spec_values[i].strip() if i < len(spec_values) else ''
            note = spec_notes[i].strip() if i < len(spec_notes) else ''
            stype = spec_types[i] if i < len(spec_types) else 'provisional'

            entry = {'value': val, 'note': note}
            if stype == 'verified':
                new_verified[k] = entry
            else:
                new_provisional[k] = entry

        product.provisional_specs = new_provisional
        product.verified_specs = new_verified
        product.save()

        messages.success(self.request, f"Product '{product.name}' specifications updated successfully.")
        return redirect('dashboard:product_edit', slug=product.slug)


class DashboardFAQListView(AdminRequiredMixin, ListView):
    model = FAQ
    template_name = 'dashboard/faq_list.html'
    context_object_name = 'faqs'

    def get_queryset(self):
        return FAQ.objects.order_by('category', 'display_order', 'id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group FAQs by Category
        grouped = {}
        for f in context['faqs']:
            cat_display = f.get_category_display()
            if cat_display not in grouped:
                grouped[cat_display] = []
            grouped[cat_display].append(f)
        context['grouped_faqs'] = grouped
        return context


class DashboardFAQCreateView(AdminRequiredMixin, CreateView):
    model = FAQ
    form_class = DashboardFAQForm
    template_name = 'dashboard/faq_form.html'
    success_url = reverse_lazy('dashboard:faq_list')

    def form_valid(self, form):
        messages.success(self.request, "New FAQ created successfully.")
        return super().form_valid(form)


class DashboardFAQUpdateView(AdminRequiredMixin, UpdateView):
    model = FAQ
    form_class = DashboardFAQForm
    template_name = 'dashboard/faq_form.html'
    success_url = reverse_lazy('dashboard:faq_list')

    def form_valid(self, form):
        messages.success(self.request, "FAQ updated successfully.")
        return super().form_valid(form)


class DashboardFAQDeleteView(AdminRequiredMixin, DeleteView):
    model = FAQ
    template_name = 'dashboard/faq_confirm_delete.html'
    success_url = reverse_lazy('dashboard:faq_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "FAQ question deleted.")
        return super().delete(request, *args, **kwargs)


# ==============================================================================
# COMPANY PROFILE, TRADE REGISTRATIONS & SOCIAL CHANNELS
# ==============================================================================

class DashboardCompanySettingsView(AdminRequiredMixin, View):
    template_name = 'dashboard/settings.html'

    def get(self, request, *args, **kwargs):
        profile = CompanyProfile.get_solo()
        profile_form = DashboardCompanyProfileForm(instance=profile)
        social_form = DashboardSocialLinkForm()
        social_links = SocialLink.objects.all().order_by('display_order', 'id')
        return render(request, self.template_name, {
            'profile': profile,
            'profile_form': profile_form,
            'social_form': social_form,
            'social_links': social_links,
        })

    def post(self, request, *args, **kwargs):
        profile = CompanyProfile.get_solo()
        profile_form = DashboardCompanyProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Company profile, trade registrations (GSTIN/IEC) & disclaimer updated successfully.")
            return redirect('dashboard:settings')
        
        social_form = DashboardSocialLinkForm()
        social_links = SocialLink.objects.all().order_by('display_order', 'id')
        messages.error(request, "Please review the form errors below.")
        return render(request, self.template_name, {
            'profile': profile,
            'profile_form': profile_form,
            'social_form': social_form,
            'social_links': social_links,
        })


class DashboardSocialLinkCreateView(AdminRequiredMixin, CreateView):
    model = SocialLink
    form_class = DashboardSocialLinkForm
    template_name = 'dashboard/social_form.html'
    success_url = reverse_lazy('dashboard:settings')

    def form_valid(self, form):
        messages.success(self.request, f"Social channel '{form.instance.display_name}' added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Failed to add social channel. Please review the inputs.")
        return redirect('dashboard:settings')


class DashboardSocialLinkUpdateView(AdminRequiredMixin, UpdateView):
    model = SocialLink
    form_class = DashboardSocialLinkForm
    template_name = 'dashboard/social_form.html'
    success_url = reverse_lazy('dashboard:settings')

    def form_valid(self, form):
        messages.success(self.request, f"Social channel '{form.instance.display_name}' updated.")
        return super().form_valid(form)


class DashboardSocialLinkDeleteView(AdminRequiredMixin, DeleteView):
    model = SocialLink
    template_name = 'dashboard/social_confirm_delete.html'
    success_url = reverse_lazy('dashboard:settings')

    def delete(self, request, *args, **kwargs):
        link = self.get_object()
        messages.success(self.request, f"Social channel '{link.display_name}' removed.")
        return super().delete(request, *args, **kwargs)


class DashboardSocialLinkToggleView(AdminRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        link = get_object_or_404(SocialLink, pk=pk)
        link.is_active = not link.is_active
        link.save()
        status_str = "visible on website" if link.is_active else "hidden from website"
        messages.success(request, f"'{link.display_name}' is now {status_str}.")
        return redirect('dashboard:settings')

